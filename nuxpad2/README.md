# Nuxpad 2.2.8

**Friendly. Fast. Focused.**

Nuxpad 2 is a lightweight cross-platform plain-text editor built with Python and PyQt6.

## Portable source layout

The current source release uses the common Pythoine portable layout:

```text
main.py
suite-pythoine-component.json
nuxpad2/
```

`main.py` is the canonical source-portable entrypoint. The application implementation, assets, documentation, QA and platform packaging live beneath `nuxpad2/`.

## Configuration

Linux:

```text
~/.config/brunonlinespace/nuxpad2/nuxpad.json
```

Windows:

```text
%APPDATA%\brunonlinespace\Nuxpad2\nuxpad.json
```

## Packaging

The Fedora AppImage builder is:

```text
nuxpad2/packaging/fedora/build-appimage.sh
```

The Windows portable builder is:

```text
nuxpad2/windows/build-windows-portable.ps1
```
