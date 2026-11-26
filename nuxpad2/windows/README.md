# Nuxpad 2 Windows portable build

Run `build-windows-portable.ps1` from Windows with Python available.

The builder uses the same project-root `main.py`, `nuxpad2/requirements.txt`, and canonical application assets as the Linux/source-portable build.

Outputs the `Nuxpad-2.2.8-Windows-x64-portable` folder/ZIP plus checksum, build-info and Python-lock records. It does not install file associations or write Windows registry entries.
