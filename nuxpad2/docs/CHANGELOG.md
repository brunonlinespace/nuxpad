# Changelog

## 2.3.4

- Give the non-Retro **Keyboard Shortcuts** dialog dialog-specific Dark/Light styling aligned to the LinSpectacles Kernel Modules 1.0.5-exp1 authority for the shared controls, while deliberately retaining Nuxpad's existing font face.
- Enable alternating shortcut-table rows, 4 px table radius, bold headers, and the matching authority colours, borders, buttons, focus states, and scrollbars.
- Soften **Nuxpad Light** editor canvas from pure white to `#f3f3f3` while retaining the existing `#202020` foreground and the rest of the light-canvas treatment.
- Add the separate **Black on White** editor preset using `#000000` on `#ffffff`.
- Preserve the 2.3.3 Find-filter startup hotfix and all accepted 2.3.2 corrections.
- No unrelated editor-engine, file-handling, About, native-dialog, packaging, Retro-asset, or source-tree changes.

## 2.3.3

- Fix the 2.3.2 startup crash in the Find Escape-focus handling.
- Install the event filters only after both Find entries have been created.
- Preserve the intended **Esc returns focus to the editor canvas** behaviour.
- No other functional change from 2.3.2.

## 2.3.2

- Rename the Edit menu entry to **Symbols…** and assign `Shift+F5`.
- Relabel the in-toolbar Editor Layout modes to **Find In-line**.
- Make `Esc` in either Find entry return focus to the editor canvas.
- Re-resolve one common toolbar/menu/List/Symbols/Find control height after layout or shell-style changes so split and in-line modes stay visually aligned.
- Reapply the Retro program font after the runtime style/QSS switch so Windows Light/Dark changes do not leave existing controls on the native font until restart.
- Preserve the existing success-only cleanup of `nuxpad2\build\windows-x64` in the Windows builder.
- No unrelated editor-engine, file-handling, About, native-dialog, packaging, or theme-colour changes.

## 2.3.1

- Add **File → Properties** directly below Rename with `F4`.
- Add **Edit → List** and **Edit → Symbols** between Paste and Date + Time as a separated block.
- Add **Edit → Find** immediately before Go To Line.
- Replace the old hard-coded Keyboard Shortcuts dialog with a searchable, menu-filtered live QAction inventory.
- Make the Keyboard Shortcuts dialog modeless, single-instance, and synchronized to Nuxpad's live File/Edit/View/Help actions.
- Reorder the lower View blocks as **Editor Layout**, **Editor Font…**, **App Theme**, and **App Drag-and-Drop**.
- Relabel Editor Layout to the four Toolbar/Find arrangements, make **Toolbar Top / Find Bottom** the default, and bind them to `Ctrl+1` through `Ctrl+4`.
- No unrelated editor-engine, file-handling, theme, About, native-dialog, packaging, or source-tree changes.

## 2.3.0

- Replace **Dark Editor** with the exclusive **Editor Colours** submenu while preserving Nuxpad Dark/Light and adding the seven approved additional colour pairs.
- Replace the Windows-folder README with the approved detailed build instructions.
- Remove the temporary Windows build workspace after a fully successful build while retaining it on failure.
- Keep only `Nuxpad.exe`, `_internal\`, and the master `README.md` visible at the Windows portable root; supporting documentation is bundled internally.
- No unrelated editor-engine or application behaviour changes.

## 2.2.8

- Remove all icons from AppMenu actions.
- Rename **Font…** to **Display Font…**.
- Move **Date + Time** before **Date**, producing **Date + Time → Date → Time**.
- Update the project repository to `https://github.com/brunonlinespace/nuxpad`.
- Replace the previous two-editor comparison with the approved classic Microsoft Notepad description.
- Synchronize application, AppImage, Windows, Suite component, AppStream, documentation, and release-gate identity to 2.2.8.

## 2.1.0-r2

- Packaging-metadata hotfix: add the required AppStream release date (`2026-09-24`) for the current release.
- Expand the first AppStream description paragraph so validation no longer reports `description-first-para-too-short`.
- Add release-gate coverage for the current AppStream release date and minimum description length.
- No editor, workflow, routing, printing, or UI behavior changes beyond the synchronized revision identity.

## 2.1.0-r1

- Packaging-only hotfix: corrected the PyInstaller build-requirements file so the build-only dependency is installed in the isolated AppImage environment.
- Added release-gate coverage for malformed literal `\n` sequences in the build requirements.
- No editor, workflow, routing, printing, or UI behavior changes.

## 2.1.0

- Harmonised the source tree around project-root `main.py` plus `nuxpad2/`.
- Rebased Fedora AppImage packaging onto the hardened non-privileged Pythoine contract.
- Added Suite Pythoine component metadata and modern Desktop/AppStream metadata.
- Kept Nuxpad-specific QtPrintSupport/printing behavior; no QtPdf reader dependency was introduced.
- Aligned About and the slogan to **Friendly. Fast. Focused.**
- Preserved the 2.0.0-rc5.1 editor behavior and cross-platform configuration paths.


## 2.0.0-rc5.1

- Correct Windows organisation, AppUserModelID, QCoreApplication organisation,
  executable CompanyName, and preference path to `brunonlinespace`.
- Migrate the earlier `BrunoOnlineSpace` preference directory.
- Replace the toolbar List icon with `• List`.
- Remove the narrow fixed width that truncated the Windows label.
- Tint AppImage icons for dark/light contrast and refresh them immediately.
- Keep Portable Linux and Windows icon handling unchanged.

## 2.0.0-rc5.1

- Promote the shared Linux/Windows codebase to mainline.
- Retire the separate Linux RC4 and XP experimental branch.
- Add official Windows x64 portable packaging.
- Keep AppImage dark/light themes isolated from Portable Linux and Windows.
- Launch Linux host character-map utilities with a sanitised environment.
- Strengthen external-change detection with SHA-256 content signatures.
- Correct Linux-only product language to Linux and Windows.
- Archive XP development/test records under `docs/history/`.

## Pre-publication candidates

RC1 through RC4 and XP1/XP2 were unpublished development candidates used to complete source QA, packaging, cross-platform adaptation, and reliability corrections before the first stable public release.
