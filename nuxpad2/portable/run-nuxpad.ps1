$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& python (Join-Path $ProjectRoot "main.py") @args
exit $LASTEXITCODE
