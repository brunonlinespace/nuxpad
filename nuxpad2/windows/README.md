# Nuxpad 2 Windows portable build

This folder contains the PowerShell builder for the self-contained **Nuxpad 2 Windows x64 portable package**.

The builder uses the same project-root `main.py`, canonical `nuxpad2/source/nuxpad.py`, runtime requirements, application assets, and documentation as the source-portable and Linux builds.

## Requirements

Build on **Windows x64** with:

- Python 3 available from PowerShell;
- internet access when the isolated build environment needs to install Python build dependencies;
- PowerShell permission to run the build script.

The builder does not install Nuxpad system-wide.

## Running the builder

### From the repository root

Open PowerShell in the repository root.

If PowerShell blocks local scripts, allow scripts for the **current PowerShell process only**:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Then run:

```powershell
.\nuxpad2\windows\build-windows-portable.ps1
```

### From `nuxpad2\windows`

If PowerShell is already open in the `nuxpad2\windows` folder:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\build-windows-portable.ps1
```

If your current PowerShell execution policy already allows the script to run, the `Set-ExecutionPolicy` command is not required.

## What the builder does

The builder:

1. confirms that it is running on Windows;
2. checks that the required source, icon, requirements, and Windows version-information files exist;
3. verifies that the canonical Nuxpad source reports the expected application version;
4. creates a clean isolated Python virtual environment under `nuxpad2\build\windows-x64`;
5. updates `pip`, `wheel`, and `setuptools` inside that environment;
6. installs the Nuxpad runtime requirements and PyInstaller build requirements;
7. runs `pip check`;
8. compiles the source with Python's `compileall` as a syntax check;
9. records the complete Python environment with `pip freeze --all`;
10. verifies the source-portable version output;
11. builds the Windows application with PyInstaller in `--windowed --onedir` mode;
12. assembles the portable package with Nuxpad assets and internal supporting documentation;
13. verifies the frozen `Nuxpad.exe` version;
14. runs a short GUI launch smoke test unless explicitly skipped;
15. creates the portable ZIP, SHA-256 checksum, build-information record, and Python-lock record;
16. removes the temporary `nuxpad2\build\windows-x64` workspace after all build outputs and records have been created successfully.

If the build fails before completion, the temporary build workspace is left in place for diagnosis.

## Build options

### Skip the GUI smoke test

The normal build includes a short launch test of the frozen executable.

To skip that test:

```powershell
.\nuxpad2\windows\build-windows-portable.ps1 -SkipSmokeTest
```

Use this only when you deliberately do not want the normal GUI smoke-test gate.

### Use a different Python command

The builder uses `python` by default.

To select another Python command:

```powershell
.\nuxpad2\windows\build-windows-portable.ps1 -PythonCommand py
```

or, for example:

```powershell
.\nuxpad2\windows\build-windows-portable.ps1 -PythonCommand python3
```

The selected command must be able to create the isolated virtual environment.

## Outputs

Successful builds are written under:

```text
nuxpad2\dist\
```

For Nuxpad 2.3.4, the expected outputs are:

```text
Nuxpad-2.3.4-Windows-x64-portable\
Nuxpad-2.3.4-Windows-x64-portable.zip
Nuxpad-2.3.4-Windows-x64-portable.zip.sha256
Nuxpad-2.3.4-Windows-x64.build-info.txt
Nuxpad-2.3.4-Windows-x64.build-python-lock.txt
```

The visible portable-folder root contains `Nuxpad.exe`, the PyInstaller `_internal\` runtime directory, and the master `README.md`. Supporting licence/release/architecture documentation is bundled inside `_internal\`; no visible root-level `docs\` folder is created.

## What the builder does not do

The Windows builder does **not**:

- install Nuxpad into Windows;
- create file associations;
- create or modify Nuxpad registry entries;
- require a system-wide PyInstaller installation;
- reuse the host Python environment for the packaged application.

Build dependencies are installed into the isolated build environment created under `nuxpad2\build\windows-x64`. That temporary workspace is removed only after a successful build; it is retained when a build fails.

## Troubleshooting

### PowerShell says running scripts is disabled

Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

and then run the builder again in the same PowerShell window.

### `python` is not found

Confirm that Python is installed and available from PowerShell:

```powershell
python --version
```

If your Windows Python installation uses another command, pass it explicitly:

```powershell
.\nuxpad2\windows\build-windows-portable.ps1 -PythonCommand py
```

### The GUI smoke test fails

Do not treat a failed smoke test as a successful release build. Review the failure first.

`-SkipSmokeTest` is available for deliberate diagnostic or packaging work, but the normal release build is expected to pass the smoke test.

## Packaging model

The Windows release is a **portable folder plus ZIP**. Users can extract the ZIP and run `Nuxpad.exe` directly.

The portable root deliberately exposes only the executable, PyInstaller's `_internal\` directory, and the master `README.md`; supporting documentation remains internal.

No installer is produced by this builder.
