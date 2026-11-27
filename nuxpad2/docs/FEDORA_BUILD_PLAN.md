# Nuxpad 2.3.4 Fedora AppImage build

Use:

```bash
chmod +x nuxpad2/packaging/fedora/build-appimage.sh
./nuxpad2/packaging/fedora/build-appimage.sh
```

The builder is non-privileged: it checks host prerequisites but does not run `sudo`, `dnf`, `pkexec`, or `su`.

Validated build hosts are Fedora 43/44 on native x86_64 or aarch64. Finished artifacts are written to `nuxpad2/dist/`.
