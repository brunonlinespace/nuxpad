# Nuxpad 2.3.4 — Final QA Checklist

## Launch and configuration

- [ ] Launch from source on the primary Fedora test system
- [ ] Confirm About shows version 2.3.4
- [ ] Confirm configuration is written to:
      `~/.config/brunonlinespace/nuxpad2/nuxpad.json`
- [ ] Confirm migration from older configuration locations
- [ ] Confirm a malformed config does not prevent launch

## File operations

- [ ] New
- [ ] Open
- [ ] Save
- [ ] Save As adds `.txt` only when no extension was entered
- [ ] Rename updates the on-disk file, title bar, and status bar
- [ ] Rename refuses folder paths
- [ ] Rename replacement confirmation works
- [ ] Properties opens from File below Rename and with F4
- [ ] Unsaved-change Save / Discard / Cancel prompts work
- [ ] New Window works
- [ ] Multiple command-line files open correctly

## Drag and drop

- [ ] Active-window mode with a saved document
- [ ] Active-window mode with unsaved changes
- [ ] New-window mode leaves the active document untouched
- [ ] Multiple dropped files
- [ ] Unsupported or binary files are rejected safely

## Editing and shortcuts

- [ ] Undo: Ctrl+Z
- [ ] Redo: Ctrl+Y
- [ ] Cut / Copy / Paste / Select All
- [ ] List: Ctrl+L
- [ ] Symbols…: Shift+F5
- [ ] Rename: F2
- [ ] Date + Time: F5
- [ ] Date Only: Ctrl+;
- [ ] Time Only: Ctrl+:
- [ ] Find: Ctrl+F
- [ ] Go To Line: Ctrl+G
- [ ] Replace: Ctrl+H
- [ ] Keyboard Shortcuts dialog is modeless, searchable, menu-filtered, single-instance, and matches actual bindings
- [ ] Keyboard Shortcuts non-Retro Dark matches the Kernel Modules authority except for font face
- [ ] Keyboard Shortcuts non-Retro Light matches the Kernel Modules authority except for font face
- [ ] Keyboard Shortcuts table uses alternating rows, bold headers, and the authority border/radius treatment

## Interface

- [ ] Editor Layout: Toolbar Top / Find Bottom (Ctrl+1, default)
- [ ] Editor Layout: Toolbar Top / Find In-line (Ctrl+2)
- [ ] Editor Layout: Toolbar Bottom / Find Top (Ctrl+3)
- [ ] Editor Layout: Toolbar Bottom / Find In-line (Ctrl+4)
- [ ] Menu Only on and off
- [ ] Status Bar on and off
- [ ] Full path appears on the left of the status bar
- [ ] Counters update on the right
- [ ] Line-number gutter keeps the Qt UI font
- [ ] User font changes affect only document text
- [ ] Symbols popup inserts characters and restores focus
- [ ] Esc in either Find field returns focus to the editor canvas
- [ ] Menu/List/Symbols/Find controls retain equal height in split and in-line layouts
- [ ] More Symbols opens an available character-map utility
- [ ] AppMenu actions display no icons
- [ ] Edit menu exposes List and Symbols between Paste and Date + Time, with separators
- [ ] Edit menu exposes Find immediately before Go To Line
- [ ] Date/time order remains Date + Time → Date → Time
- [ ] View lower blocks are Editor Layout → Editor Font… → App Theme → App Drag-and-Drop
- [ ] View menu spacing and labels are correct
- [ ] Nuxpad Light uses `#202020` text on `#f3f3f3`
- [ ] Black on White uses `#000000` text on `#ffffff`
- [ ] Retro program font remains correct after runtime Light/Dark switching on Windows
- [ ] About uses the approved classic Microsoft Notepad description
- [ ] About repository link is https://github.com/brunonlinespace/nuxpad

## Encoding and content safety

- [ ] UTF-8 without BOM
- [ ] UTF-8 with BOM
- [ ] UTF-16 LE/BE
- [ ] UTF-32 LE/BE
- [ ] Windows-1252 fallback
- [ ] ISO-8859-1 fallback
- [ ] Original BOM is preserved
- [ ] Original encoding is preserved
- [ ] Unrepresentable characters cancel saving safely
- [ ] Symlink and permission behaviour remains correct
- [ ] Large-file opening remains acceptable

## `.LOG`

- [ ] First line exactly `.LOG` appends a timestamp on open
- [ ] Similar text does not trigger `.LOG`
- [ ] Timestamp uses the system locale
- [ ] Document is marked modified but not auto-saved

## Printing and PDF

- [ ] Small document prints to PDF
- [ ] Multi-page document prints to PDF
- [ ] Body text is solid black
- [ ] Header and footer do not overlap body text
- [ ] Left, centre, and right fields align correctly
- [ ] All placeholders expand correctly
- [ ] Header/footer enable toggles work
- [ ] Page Setup preferences persist

## Cross-desktop release testing

- [ ] KDE Plasma Wayland
- [ ] GNOME Wayland
- [ ] XFCE/X11
- [ ] System without PyQt6 installed — after AppImage build
- [ ] Desktop launcher icon
- [ ] Open With Nuxpad
- [ ] `%F` multiple-file desktop handling
- [ ] Printing from the packaged build

## Release gate

- [ ] No known crash
- [ ] No known data-loss bug
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] GPLv3 licence included
- [ ] AppImage built
- [ ] AppImage SHA-256 generated
- [ ] GitHub release draft prepared
