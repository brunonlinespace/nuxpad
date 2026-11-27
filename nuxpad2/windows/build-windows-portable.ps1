param(
    [switch]$SkipSmokeTest,
    [string]$PythonCommand = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$AppName = "Nuxpad"
$DisplayName = "Nuxpad 2"
$Version = "2.3.4"
$Architecture = "x64"

if ([System.Environment]::OSVersion.Platform -ne [System.PlatformID]::Win32NT) {
    throw "This build script must be run on Windows."
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProgramRoot = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $ProgramRoot
$SourceEntry = Join-Path $ProjectRoot "main.py"
$IconDir = Join-Path $ProgramRoot "assets\icons"
$IconFile = Join-Path $IconDir "nuxpad.ico"
$AboutImage = Join-Path $IconDir "nuxpad-about.png"
$RuntimeRequirements = Join-Path $ProgramRoot "requirements.txt"
$BuildRequirements = Join-Path $ProgramRoot "packaging\pyinstaller\build-requirements.txt"
$VersionInfo = Join-Path $ScriptDir "windows-version-info.txt"

$BuildRoot = Join-Path $ProgramRoot "build\windows-x64"
$Venv = Join-Path $BuildRoot "venv"
$VenvPython = Join-Path $Venv "Scripts\python.exe"
$PyInstaller = Join-Path $Venv "Scripts\pyinstaller.exe"
$PyInstallerDist = Join-Path $BuildRoot "pyinstaller-dist"
$PyInstallerWork = Join-Path $BuildRoot "pyinstaller-work"
$Dist = Join-Path $ProgramRoot "dist"
$PackageName = "$AppName-$Version-Windows-$Architecture-portable"
$PackageDir = Join-Path $Dist $PackageName
$ZipFile = Join-Path $Dist "$PackageName.zip"
$ChecksumFile = "$ZipFile.sha256"
$BuildInfo = Join-Path $Dist "$AppName-$Version-Windows-$Architecture.build-info.txt"
$PythonLock = Join-Path $Dist "$AppName-$Version-Windows-$Architecture.build-python-lock.txt"

function Write-Step([string]$Message) {
    Write-Host ""
    Write-Host "==> $Message"
}

function Assert-File([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Missing required file: $Path"
    }
}

foreach ($Required in @(
    $SourceEntry, $IconFile, $AboutImage, $RuntimeRequirements,
    $BuildRequirements, $VersionInfo
)) {
    Assert-File $Required
}

$CanonicalSource = Join-Path $ProgramRoot "source\nuxpad.py"
$SourceText = Get-Content -LiteralPath $CanonicalSource -Raw
$ExpectedVersionPattern = (
    'APP_VERSION\s*=\s*"' +
    [regex]::Escape($Version) +
    '"'
)
if ($SourceText -notmatch $ExpectedVersionPattern) {
    throw "Canonical source version mismatch. Expected $Version."
}

Write-Step "Preparing isolated Python environment"
if (Test-Path -LiteralPath $BuildRoot) {
    Remove-Item -LiteralPath $BuildRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $BuildRoot, $Dist -Force | Out-Null

& $PythonCommand -m venv $Venv
if ($LASTEXITCODE -ne 0) { throw "Could not create the Python virtual environment." }

& $VenvPython -m pip install --upgrade pip wheel setuptools
if ($LASTEXITCODE -ne 0) { throw "Could not update the Python build tools." }

& $VenvPython -m pip install -r $RuntimeRequirements -r $BuildRequirements
if ($LASTEXITCODE -ne 0) { throw "Could not install the Windows build requirements." }

& $VenvPython -m pip check
if ($LASTEXITCODE -ne 0) { throw "Python dependency check failed." }

& $VenvPython -m compileall -q $SourceEntry $ProgramRoot
if ($LASTEXITCODE -ne 0) { throw "The source failed Python syntax validation." }

& $VenvPython -m pip freeze --all |
    Set-Content -LiteralPath $PythonLock -Encoding UTF8

$ReportedVersion = (& $VenvPython $SourceEntry --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $ReportedVersion -ne "$DisplayName $Version") {
    throw "Portable version probe failed: $ReportedVersion"
}

Write-Step "Building the Windows portable application"
$PyInstallerArguments = @(
    "--noconfirm",
    "--clean",
    "--windowed",
    "--onedir",
    "--optimize", "1",
    "--name", "Nuxpad",
    "--icon", $IconFile,
    "--version-file", $VersionInfo,
    "--distpath", $PyInstallerDist,
    "--workpath", $PyInstallerWork,
    "--specpath", $BuildRoot,
    "--paths", $ProjectRoot,
    "--add-data", "$($ProgramRoot)\assets;nuxpad2\assets",
    "--add-data", "$($ProgramRoot)\LICENSE;.",
    "--add-data", "$($ProgramRoot)\docs\CROSS_PLATFORM_ARCHITECTURE.md;docs",
    "--add-data", "$($ProgramRoot)\docs\RELEASE_NOTES.md;docs",
    $SourceEntry
)
& $PyInstaller @PyInstallerArguments
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed." }

Write-Step "Assembling the portable Windows package"
if (Test-Path -LiteralPath $PackageDir) {
    Remove-Item -LiteralPath $PackageDir -Recurse -Force
}
New-Item -ItemType Directory -Path $PackageDir | Out-Null
Copy-Item -Path (Join-Path $PyInstallerDist "Nuxpad\*") `
    -Destination $PackageDir -Recurse -Force
Copy-Item -LiteralPath (Join-Path $ProjectRoot "README.md") `
    -Destination (Join-Path $PackageDir "README.md")

$Executable = Join-Path $PackageDir "Nuxpad.exe"
$BuiltVersion = (& $Executable --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $BuiltVersion -ne "$DisplayName $Version") {
    throw "Frozen executable version probe failed: $BuiltVersion"
}

if (-not $SkipSmokeTest) {
    Write-Step "Running a short Windows launch smoke test"
    $Process = Start-Process -FilePath $Executable -ArgumentList "--nuxpad-smoke-test" -PassThru
    if (-not $Process.WaitForExit(30000)) {
        Stop-Process -Id $Process.Id -Force
        throw "Nuxpad GUI smoke test timed out."
    }
    if ($Process.ExitCode -ne 0) {
        throw "Nuxpad exited during the smoke test with code $($Process.ExitCode)."
    }
}

Write-Step "Creating the portable ZIP and build records"
if (Test-Path -LiteralPath $ZipFile) {
    Remove-Item -LiteralPath $ZipFile -Force
}
Compress-Archive -LiteralPath $PackageDir -DestinationPath $ZipFile `
    -CompressionLevel Optimal

$Hash = (Get-FileHash -LiteralPath $ZipFile -Algorithm SHA256).Hash.ToLowerInvariant()
"$Hash  $(Split-Path -Leaf $ZipFile)" |
    Set-Content -LiteralPath $ChecksumFile -Encoding ASCII

$PythonVersion = (& $VenvPython --version 2>&1 | Out-String).Trim()
$PyInstallerVersion = (& $PyInstaller --version 2>&1 | Out-String).Trim()
$QtVersions = (& $VenvPython -c `
    "from PyQt6.QtCore import PYQT_VERSION_STR, QT_VERSION_STR; print('PyQt6:', PYQT_VERSION_STR); print('Qt:', QT_VERSION_STR)" `
    2>&1 | Out-String).Trim()
$SourceHash = (Get-FileHash -LiteralPath $CanonicalSource -Algorithm SHA256).Hash.ToLowerInvariant()

@"
Nuxpad Windows build
Version: $Version
Architecture: $Architecture
Built: $(Get-Date -Format o)
Host: $([System.Environment]::OSVersion.VersionString)
Python: $PythonVersion
PyInstaller: $PyInstallerVersion
$QtVersions
Canonical source SHA-256: $SourceHash
Output: $(Split-Path -Leaf $ZipFile)
Output SHA-256: $Hash
"@ | Set-Content -LiteralPath $BuildInfo -Encoding UTF8

Write-Step "Cleaning temporary Windows build files"
Remove-Item -LiteralPath $BuildRoot -Recurse -Force

Write-Step "Build complete"
Write-Host $PackageDir
Write-Host $ZipFile
Write-Host $ChecksumFile
Write-Host $BuildInfo
Write-Host $PythonLock
