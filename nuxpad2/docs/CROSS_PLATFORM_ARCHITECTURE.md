# Nuxpad 2 cross-platform architecture

Nuxpad 2.3.4 uses one shared PyQt6 application implementation:

```text
nuxpad2/source/nuxpad.py
```

The project-root `main.py` is the canonical Portable entrypoint on every platform.

Linux preferences:

```text
~/.config/brunonlinespace/nuxpad2/nuxpad.json
```

Windows preferences:

```text
%APPDATA%\brunonlinespace\Nuxpad2\nuxpad.json
```

Linux AppImage-specific themes remain isolated to the AppImage runtime. Source-portable Linux and Windows continue to use the host Qt style.
