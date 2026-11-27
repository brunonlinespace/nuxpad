# Nuxpad 2 feature-freeze status

Nuxpad 2.3.4 preserves the established plain-text editor workflow and the accepted 2.3.x interface, theme, and packaging architecture.

The 2.3.0–2.3.4 work is limited to the approved changes below:

- replace **Dark Editor** with the exclusive **Editor Colours** submenu;
- retain **Nuxpad Dark**, soften **Nuxpad Light** to `#202020` on `#f3f3f3`, and provide the approved additional editor colour presets including **Black on White**;
- add **File → Properties** with `F4`;
- expose **List**, **Symbols…**, and **Find** as live Edit-menu actions, with **Symbols…** on `Shift+F5`;
- replace the hard-coded Keyboard Shortcuts view with the searchable, menu-filtered, modeless live QAction inventory;
- align that dialog's non-Retro Dark/Light presentation to the LinSpectacles Kernel Modules 1.0.5-exp1 authority while retaining Nuxpad's existing font face;
- use the approved **Editor Layout / Editor Font… / App Theme / App Drag-and-Drop** View structure and the four `Ctrl+1` through `Ctrl+4` layout shortcuts;
- use **Find In-line** wording for the two in-toolbar Find layouts;
- return focus from either Find entry to the editor canvas with `Esc`;
- keep toolbar/menu/List/Symbols/Find control heights synchronized across split and in-line layouts;
- retain the Windows Retro-font runtime correction;
- use the approved detailed Windows build README;
- remove the temporary Windows build workspace only after a fully successful Windows build, leaving it available on failure;
- keep supporting Windows portable documentation internal while the master README remains visible at the portable root.

No unrelated editor-engine, file-handling, encoding, search/replace, printing, About, native-dialog, or source-tree changes are part of this feature-freeze baseline.
