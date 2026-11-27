# Nuxpad 2.3.4

Nuxpad 2.3.4 is a tightly scoped menu, shortcut-inventory, and document-information release based directly on 2.3.0.

## File

- Adds **Properties** directly below **Rename…**.
- Adds the **F4** shortcut.
- Properties reports file location/details and current plain-text document information without modifying the document.

## Edit

- Adds **List** and **Symbols** between Paste and Date + Time, separated as their own menu block.
- Adds **Find** immediately before **Go To Line…**.
- The existing `Ctrl+L` List and `Ctrl+F` Find shortcuts now belong to these live Edit-menu actions instead of separate hidden actions.

## View

- Keeps the existing View items through **Editor Colours**.
- Renames and reorders the remaining blocks as:
  - **Editor Layout**
  - **Editor Font…**
  - **App Theme**
  - **App Drag-and-Drop**
- Editor Layout now uses:
  - **Toolbar Top / Find Bottom** — `Ctrl+1` — default
  - **Toolbar Top / Find Top** — `Ctrl+2`
  - **Toolbar Bottom / Find Top** — `Ctrl+3`
  - **Toolbar Bottom / Find Bottom** — `Ctrl+4`

## Keyboard Shortcuts

- Replaces the old hard-coded modal shortcut list with the searchable live QAction inventory pattern used by the other Pad editors.
- The dialog is modeless and single-instance.
- It provides **Command / Shortcut** columns, command/shortcut search, a **Menu:** filter, fuzzy shortcut matching, and a no-results state.
- The inventory is collected recursively from Nuxpad's live File, Edit, View, and Help menus so menu shortcut changes stay synchronized automatically.

## Scope

No unrelated editor-engine, file-handling, search/replace, printing, theme, About, native-dialog, packaging, or source-tree behaviour is changed.
