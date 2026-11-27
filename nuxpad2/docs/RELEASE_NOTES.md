# Nuxpad 2.3.4

Nuxpad 2.3.4 is the current corrective source release, built directly from the accepted 2.3.3 baseline. It retains the established plain-text editor engine while completing the approved 2.3.x menu, shortcut, editor-colour, theme-parity, and Windows-packaging work.

## File

- **Properties** sits directly below **Rename** in the File menu and uses `F4`.
- Properties reports file location/details and current plain-text document information without modifying the document.

## Edit

- **List** and **Symbols…** appear between Paste and Date + Time as their own separated block.
- **List** uses `Ctrl+L`.
- **Symbols…** uses `Shift+F5`.
- **Find** appears immediately before **Go To Line…** and uses `Ctrl+F`.
- These commands are live menu actions and are therefore discovered automatically by the Keyboard Shortcuts inventory.

## View and layouts

The lower View structure is:

- **Editor Layout**
- **Editor Font…**
- **App Theme**
- **App Drag-and-Drop**

Editor Layout uses:

- **Toolbar Top / Find Bottom** — `Ctrl+1` — default
- **Toolbar Top / Find In-line** — `Ctrl+2`
- **Toolbar Bottom / Find Top** — `Ctrl+3`
- **Toolbar Bottom / Find In-line** — `Ctrl+4`

`Esc` in either Find entry returns focus to the editor canvas.

Toolbar/menu/List/Symbols/Find controls are kept at one resolved height so split and in-line layouts remain visually aligned.

## Keyboard Shortcuts

The old hard-coded shortcut list is replaced by the searchable live QAction inventory pattern used by the other Pad editors.

The dialog is:

- modeless;
- single-instance;
- searchable by command or shortcut;
- filterable by menu;
- populated recursively from Nuxpad's live File, Edit, View, and Help menus;
- able to match modifier-order variations when searching shortcuts.

For non-Retro Dark and Light themes, the dialog now uses dialog-specific styling aligned to the uploaded LinSpectacles Kernel Modules 1.0.5-exp1 authority for the shared controls. This includes the authority colours, borders, focus states, buttons, scrollbars, 4 px table radius, bold headers, 5 px header padding, and alternating rows.

Nuxpad deliberately retains its existing application font face; the Kernel Modules font-family declaration is not imported.

Retro Chicago95/Raleigh shortcut-dialog styling remains unchanged.

## Editor Colours

**Editor Colours** is independent from the application shell theme.

**Nuxpad Dark** remains the default editor scheme.

**Nuxpad Light** keeps its established `#202020` foreground but now uses a softer `#f3f3f3` background instead of pure white.

The separate **Black on White** preset provides the stark classic pair:

- foreground `#000000`
- background `#ffffff`

The other approved editor colour presets remain available unchanged.

## Windows corrections

The Windows builder retains the detailed build instructions introduced in 2.3.0.

After a fully successful Windows build, the temporary `nuxpad2\build\windows-x64` workspace is removed. If a build fails, that workspace is retained for diagnosis.

Supporting Windows portable documentation remains internal to the frozen payload while the master `README.md` stays visible beside `Nuxpad.exe`.

The Retro program font is reapplied after the runtime style/QSS switch so Windows Light/Dark changes do not leave already-created controls using the native font until restart.

## 2.3.3 startup hotfix retained

The Find-field event filters are installed only after both Find entries exist. This preserves the intended `Esc` focus behaviour without the 2.3.2 construction-order startup crash.

## Scope

No unrelated editor-engine, file-handling, encoding, search/replace, printing, About, native-dialog, or source-tree behaviour is changed in 2.3.4.
