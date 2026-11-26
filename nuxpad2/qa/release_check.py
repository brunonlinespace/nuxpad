#!/usr/bin/env python3
"""Static/source release gate for Nuxpad 2.2.8."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_ROOT = PROJECT_ROOT / "nuxpad2"
SOURCE = PROGRAM_ROOT / "source" / "nuxpad.py"
SOURCE_MANIFEST = PROGRAM_ROOT / "SOURCE_MANIFEST.sha256"
COMPONENT_MANIFEST = PROJECT_ROOT / "suite-pythoine-component.json"

EXPECTED_VERSION = "2.2.8"
EXPECTED_FILES_AT_ROOT = {"README.md", "main.py", "suite-pythoine-component.json", "nuxpad2"}


def fail(message: str) -> None:
    raise SystemExit(f"RELEASE CHECK FAILED: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory() -> dict[str, str]:
    records: dict[str, str] = {}
    for path in sorted(PROJECT_ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(PROJECT_ROOT)
        parts = rel.parts
        if "__pycache__" in parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if len(parts) >= 2 and parts[0] == "nuxpad2" and parts[1] in {"build", "dist"}:
            continue
        if rel == Path("nuxpad2/SOURCE_MANIFEST.sha256"):
            continue
        records[f"./{rel.as_posix()}"] = sha256(path)
    return records


def read_manifest() -> dict[str, str]:
    if not SOURCE_MANIFEST.is_file():
        fail("SOURCE_MANIFEST.sha256 is missing")
    records: dict[str, str] = {}
    for raw in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            digest, rel = raw.split("  ", 1)
        except ValueError:
            fail(f"invalid source-manifest line: {raw!r}")
        records[rel] = digest
    return records


def check_structure() -> None:
    actual = {p.name for p in PROJECT_ROOT.iterdir()}
    if actual != EXPECTED_FILES_AT_ROOT:
        fail(f"portable root mismatch: {sorted(actual)!r}")
    required = [
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "main.py",
        COMPONENT_MANIFEST,
        PROGRAM_ROOT / "__init__.py",
        SOURCE,
        PROGRAM_ROOT / "requirements.txt",
        PROGRAM_ROOT / "identity.json",
        PROGRAM_ROOT / "packaging/fedora/build-appimage.sh",
        PROGRAM_ROOT / "packaging/pyinstaller/build-requirements.txt",
        PROGRAM_ROOT / "packaging/pyinstaller/nuxpad.spec",
        PROGRAM_ROOT / "packaging/appimage/AppRun",
        PROGRAM_ROOT / "packaging/appimage/io.github.brunonlinespace.nuxpad.desktop",
        PROGRAM_ROOT / "packaging/appimage/io.github.brunonlinespace.nuxpad.metainfo.xml",
        PROGRAM_ROOT / "windows/build-windows-portable.ps1",
        PROGRAM_ROOT / "assets/themes/kernel-modules-dark.qss",
        PROGRAM_ROOT / "assets/themes/kernel-modules-light.qss",
        PROGRAM_ROOT / "assets/themes/editor-canvas-dark.qss",
        PROGRAM_ROOT / "assets/themes/editor-canvas-light.qss",
        PROGRAM_ROOT / "assets/themes/chicago95/chicago95.qss",
        PROGRAM_ROOT / "assets/themes/chicago95/chicago95-dark.qss",
        PROGRAM_ROOT / "assets/themes/chicago95/ATTRIBUTION.md",
        PROGRAM_ROOT / "assets/themes/chicago95/CHICAGO95-CREDITS",
        PROGRAM_ROOT / "assets/themes/raleigh-dark/ATTRIBUTION.md",
        PROGRAM_ROOT / "assets/themes/raleigh-dark/RALEIGH-LICENSE",
    ]
    for path in required:
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(PROJECT_ROOT)}")


def check_identity() -> None:
    component = json.loads(COMPONENT_MANIFEST.read_text(encoding="utf-8"))
    expected = {
        "id": "nuxpad",
        "name": "Nuxpad 2",
        "component_kind": "editor",
        "extensions": [".txt", ".log", ".ini", ".cfg", ".conf"],
        "portable_command": ["main.py"],
        "version": EXPECTED_VERSION,
        "publisher_id": "brunonlinespace",
        "repository": "https://github.com/brunonlinespace/nuxpad",
        "desktop_id": "io.github.brunonlinespace.nuxpad",
        "tagline": "Friendly. Fast. Focused.",
        "capabilities": {"routing": True, "open": True, "create": True},
    }
    for key, value in expected.items():
        if component.get(key) != value:
            fail(f"component manifest mismatch for {key}: {component.get(key)!r}")

    identity = json.loads((PROGRAM_ROOT / "identity.json").read_text(encoding="utf-8"))
    if identity.get("component_id") != "nuxpad":
        fail("identity component ID mismatch")
    if identity.get("package") != "nuxpad2":
        fail("identity package mismatch")
    if identity.get("desktop_file") != "io.github.brunonlinespace.nuxpad.desktop":
        fail("identity desktop file mismatch")


def check_source() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    required = [
        'APP_NAME = "Nuxpad 2"',
        f'APP_VERSION = "{EXPECTED_VERSION}"',
        '<b>Friendly. Fast. Focused.</b>',
        'app.setDesktopFileName("io.github.brunonlinespace.nuxpad")',
        '"--nuxpad-smoke-test"',
        'print("GUI smoke test passed.", flush=True)',
        '<b>Configuration:</b>',
    ]
    for fragment in required:
        if fragment not in text:
            fail(f"source contract missing: {fragment}")
    if "<b>Simple. Fast. Focused.</b>" in text:
        fail("old slogan remains in live application source")
    approved_about = (
        "A lightweight text editor for Linux and Windows, inspired by the simplicity "
        "of the classic Microsoft Notepad."
    )
    if approved_about not in text:
        fail("approved About description is missing")
    if "https://github.com/brunonlinespace/nuxpad" not in text:
        fail("current repository URL is missing from live application source")
    if 'QAction("Display Font…", self)' not in text:
        fail("View menu Display Font label is missing")

    menu_start = text.find("    def add_menu_action(")
    menu_end = text.find("    def make_file_menu(", menu_start)
    if menu_start < 0 or menu_end < 0:
        fail("AppMenu helper could not be located")
    menu_helper = text[menu_start:menu_end]
    if "bind_portable_icon" in menu_helper or ".setIcon(" in menu_helper:
        fail("AppMenu helper still assigns icons")

    edit_start = text.find("    def make_edit_menu(")
    edit_end = text.find("    def make_view_menu(", edit_start)
    if edit_start < 0 or edit_end < 0:
        fail("Edit menu block could not be located")
    edit_menu = text[edit_start:edit_end]
    labels = [
        edit_menu.find('menu, "Date + Time"'),
        edit_menu.find('menu, "Date Only"'),
        edit_menu.find('menu, "Time Only"'),
    ]
    if any(position < 0 for position in labels) or labels != sorted(labels):
        fail("Edit menu date/time order is not Date + Time, Date Only, Time Only")
    if 'QPrintDialog, QPrinter' not in text:
        fail("Nuxpad printing dependency unexpectedly changed")
    if "PyQt6.QtPdf" in text or "PyQt6.QtWebEngine" in text:
        fail("unexpected QtPdf/WebEngine application dependency introduced")

    for required_fragment in (
        'QKeySequence("F2")',
        'QKeySequence("Ctrl+Shift+P")',
        'QKeySequence("Ctrl+;")',
        'QKeySequence("Ctrl+:")',
        'QKeySequence("Ctrl+Alt+Shift+W")',
        'QKeySequence("Ctrl+Alt+Shift+L")',
        'QKeySequence("Ctrl+Alt+Shift+E")',
        'QKeySequence("Ctrl+Alt+Shift+M")',
        'QKeySequence("Ctrl+Alt+Shift+S")',
        '"Date Only"',
        '"Time Only"',
        '"Dark Editor"',
        'menu.addMenu("Drag-and-Drop")',
        '"Opens on Active Window"',
        '"Opens on New Window"',
        '"Documentation"',
        'QKeySequence("F1")',
        '"GitHub Repository"',
        '"Raise an Issue"',
        'https://github.com/grassmunk/chicago95',
        'https://github.com/thesquash/gtk-theme-raleigh',
        '"★", "☆", "♥", "♦", "♣", "♠", "☐", "☑"',
        'screen = self.screen() or QApplication.primaryScreen()',
    ):
        if required_fragment not in text:
            fail(f"x3.2 requested UI/shortcut contract missing: {required_fragment}")

    for forbidden_fragment in (
        'menu.addMenu("Behaviour")',
        '"Drag and drop opens on active window"',
        '"Drag and drop opens on new window"',
    ):
        if forbidden_fragment in text:
            fail(f"x3.2 superseded menu label remains: {forbidden_fragment}")

    if "DOCUMENTATION_URL" in text:
        fail("Documentation still points to a web URL")
    if "def documentation_path():" not in text or "QUrl.fromLocalFile(readme)" not in text:
        fail("Documentation is not opening the bundled source-root README locally")
    if 'Path(__file__).resolve()' not in text or 'parents[2] / "README.md"' not in text:
        fail("source-root README lookup is missing")
    if 'href="https://github.com/brunonlinespace/">' not in text or "Bruno Machado</a><br>" not in text:
        fail("Bruno Machado is not linked to brunonlinespace in About")
    if '[<a href="https://github.com/brunonlinespace/">' in text:
        fail("standalone brunonlinespace profile link remains in About")
    about_renderer_start = text.find("    def apply_about_link_palette(self):")
    about_renderer_end = text.find("    def show_about_dialog(self):", about_renderer_start)
    about_renderer = text[
        about_renderer_start:about_renderer_end
        if about_renderer_end > about_renderer_start
        else len(text)
    ]
    license_pos = about_renderer.find("Licensed under the GNU General Public License v3 or later.")
    themes_pos = about_renderer.find("Themes:")
    if license_pos < 0 or themes_pos < 0 or themes_pos < license_pos:
        fail("About theme credits are not below the licence line")

    symbols_start = text.find("    def show_symbols_popup(self):")
    symbols_end = text.find("    def insert_bullet_point(self):", symbols_start)
    if symbols_start < 0 or symbols_end < 0:
        fail("Symbols chooser could not be isolated")
    symbols_block = text[symbols_start:symbols_end]
    if "Qt.WindowType.Popup" in symbols_block:
        fail("Symbols chooser is still a floating popup")
    if "geometry.center()" not in symbols_block or "popup.move(" not in symbols_block:
        fail("Symbols chooser is not centred like RiqatonyPad")

    help_start = text.find("    def make_help_menu(self):")
    help_end = text.find("    def bind_shortcuts(self):", help_start)
    help_block = text[help_start:help_end]
    expected_help_order = (
        '"Documentation"',
        '"Keyboard Shortcuts"',
        '"GitHub Repository"',
        '"Raise an Issue"',
        '"About Nuxpad 2"',
    )
    positions = [help_block.find(item) for item in expected_help_order]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        fail("Help menu order does not match x3.2")

    if not re.search(
        r'QFileDialog\.getOpenFileName\(\s*None,\s*"Open File"',
        text,
    ):
        fail("Open picker is not parentless like Path Inspector")
    if not re.search(
        r'QFileDialog\.getSaveFileName\(\s*None,\s*"Save As"',
        text,
    ):
        fail("Save As picker is not parentless like Path Inspector")
    if "QPrintDialog(printer, None)" not in text:
        fail("Print/Print to File is not parentless")
    if 'QFontDialog.getFont(current, None, "Font")' not in text:
        fail("Display Font picker is not parentless")

    open_start = text.find("    def open_file(self):")
    open_end = text.find("    @staticmethod", open_start)
    open_block = text[open_start:open_end]
    for forbidden in (
        "application_stylesheet",
        "window_stylesheets",
        "QApplication.instance()",
        ".setStyleSheet(",
    ):
        if forbidden in open_block:
            fail(f"Open contains obsolete theme workaround: {forbidden}")

    if "KERNEL_MODULES_THEME_EXPERIMENT = True" not in text:
        fail("Kernel Modules shell-theme experiment flag is missing")
    if "menu_button_height = max(" not in text:
        fail("toolbar/search button height normalization is missing")
    if "self.search_entry.setFixedHeight(menu_button_height)" not in text:
        fail("top Find entry height normalization is missing")
    if "self.bottom_search_entry.setFixedHeight(menu_button_height)" not in text:
        fail("bottom Find entry height normalization is missing")
    for button_name in (
        "self.list_button",
        "self.symbols_button",
        "self.search_button",
        "self.search_previous_button",
        "self.search_next_button",
        "self.bottom_search_button",
        "self.bottom_previous_button",
        "self.bottom_next_button",
    ):
        if button_name not in text:
            fail(f"button height normalization target missing: {button_name}")
    if "apply_kernel_modules_theme(" not in text:
        fail("Kernel Modules shell-theme helper is missing")
    if 'self.application_theme = "dark"' not in text:
        fail("shell-theme default is missing")
    if '"application_theme": self.application_theme' not in text:
        fail("shell-theme persistence is missing")
    if "QActionGroup(self)" not in text or "setExclusive(True)" not in text:
        fail("View Theme radio group is missing")
    if "self.set_application_theme(selected)" not in text:
        fail("shared View Theme callback is missing")
    if 'self.retro_theme = False' not in text:
        fail("Retro must default off so x2.6 remains the default apparatus")
    if '"retro_theme": self.retro_theme' not in text:
        fail("Retro preference persistence is missing")
    if '"Chicago95/Raleigh"' not in text or "self.toggle_retro_theme" not in text:
        fail("View Theme Chicago95/Raleigh checkmark is missing")
    if "theme_menu.addSeparator()" not in text:
        fail("Theme separator before Chicago95/Raleigh is missing")
    if "theme_menu.addAction(self.retro_theme_action)" not in text:
        fail("Chicago95/Raleigh is not inside the Theme submenu")
    if re.search(r"(?m)^\s{8}menu\.addAction\(self\.retro_theme_action\)\s*$", text):
        fail("Chicago95/Raleigh incorrectly remains a top-level View item")
    if "def apply_selected_shell_theme(self):" not in text:
        fail("merged shell-theme dispatcher is missing")
    if "apply_retro_theme(" not in text:
        fail("x1.2 Retro theme helper is missing")
    if "chicago95_theme_resources()" not in text:
        fail("x1.2 Retro resource discovery is missing")
    if 'self.setObjectName("editorCanvas")' in text:
        fail("x2.3 editorCanvas object-name intervention was not removed")
    if 'self.dark_editor_canvas = True' not in text:
        fail("Dark Editor Canvas default is missing")
    if '"dark_editor_canvas": self.dark_editor_canvas' not in text:
        fail("Dark Editor Canvas persistence is missing")
    if '"Dark Editor"' not in text:
        fail("View Dark Editor action is missing")
    if '"Dark Editor Canvas"' in text:
        fail("superseded Dark Editor Canvas visible label remains")
    if "def apply_editor_canvas_style(self):" not in text:
        fail("independent editor-canvas helper is missing")
    if 'colour = "#ffffff" if self.application_theme == "dark" else "#202020"' not in text:
        fail("theme-aware icon contrast is missing")

    dark_theme_text = (PROGRAM_ROOT / "assets/themes/kernel-modules-dark.qss").read_text(encoding="utf-8")
    light_theme_text = (PROGRAM_ROOT / "assets/themes/kernel-modules-light.qss").read_text(encoding="utf-8")
    for colour in ("#1e1e1e","#252526","#2d2d2d","#333333","#454545","#007acc","#005999","#094771","#dcdcdc"):
        if colour not in dark_theme_text.lower():
            fail(f"dark authority colour missing: {colour}")
    for colour in ("#d4d4d4","#202020","#f4f4f4","#b2b2b2","#e4e4e4","#0b64a0","#dcecf8","#c5e0f2","#303030","#b0b0b0","#8e8e8e"):
        if colour not in light_theme_text.lower():
            fail(f"dimmed light authority colour missing: {colour}")
    for theme_text in (dark_theme_text, light_theme_text):
        if re.search(r"(?im)^\s*font-family\s*:", theme_text):
            fail("shell theme overrides program font family")
        if re.search(r"(?im)^\s*font-size\s*:", theme_text):
            fail("shell theme overrides program font size")
    for shell_theme_text in (dark_theme_text, light_theme_text):
        if "QPlainTextEdit" in shell_theme_text:
            fail("application shell stylesheet still controls the editor canvas")

    editor_dark_text = (PROGRAM_ROOT / "assets/themes/editor-canvas-dark.qss").read_text(encoding="utf-8")
    editor_light_text = (PROGRAM_ROOT / "assets/themes/editor-canvas-light.qss").read_text(encoding="utf-8")
    for colour in ("#1e1e1e", "#dcdcdc", "#333333", "#094771", "#424242", "#686868"):
        if colour not in editor_dark_text.lower():
            fail(f"dark editor canvas lost x2.2 authority colour: {colour}")
    for colour in ("#ffffff", "#202020", "#b8b8b8", "#0b64a0", "#b0b0b0", "#8e8e8e"):
        if colour not in editor_light_text.lower():
            fail(f"light editor canvas colour missing: {colour}")

    set_theme_start = text.find("    def set_application_theme(")
    set_theme_end = text.find("    def effective_appimage_theme(", set_theme_start)
    set_theme_block = text[set_theme_start:set_theme_end]
    if "dark_editor_canvas" in set_theme_block or "apply_editor_canvas_style" in set_theme_block:
        fail("application shell theme is coupled to editor canvas")

    retro_light = (
        PROGRAM_ROOT / "assets/themes/chicago95/chicago95.qss"
    ).read_text(encoding="utf-8")
    retro_dark = (
        PROGRAM_ROOT / "assets/themes/chicago95/chicago95-dark.qss"
    ).read_text(encoding="utf-8")
    for marker in ("#c0c0c0", "#000080"):
        if marker not in retro_light.lower():
            fail(f"Chicago95 light authority marker missing: {marker}")
    if "__CHICAGO95_ROOT__" not in retro_light:
        fail("Chicago95 asset-root placeholder is missing")
    for colour in ("#232424", "#434444", "#49667f", "#ffffff"):
        if colour not in retro_dark.lower():
            fail(f"Raleigh dark authority colour missing: {colour}")

    if 'QFont("MS Sans Serif", 11)' not in text:
        fail("x1.2 Retro program-font apparatus was not preserved")
    if 'app.setProperty("nuxpad_original_palette", QPalette(app.palette()))' not in text:
        fail("original palette capture for Retro exit is missing")
    if 'app.setProperty("nuxpad_original_font", QFont(app.font()))' not in text:
        fail("original font capture for Retro exit is missing")

    if '"themes", "raleigh-dark", "ATTRIBUTION.md"' not in text:
        fail("Raleigh is not discovered from its own sibling theme directory")
    if '"raleigh_root": raleigh_root' not in text:
        fail("separate Raleigh root is missing from Retro resources")
    if 'stylesheet.replace("__RALEIGH_ROOT__", raleigh_root)' not in text:
        fail("Retro QSS does not substitute the separate Raleigh root")

    chicago_root = PROGRAM_ROOT / "assets/themes/chicago95"
    raleigh_root = PROGRAM_ROOT / "assets/themes/raleigh-dark"

    if (chicago_root / "raleigh-dark").exists():
        fail("Raleigh incorrectly remains nested under Chicago95")

    retro_light = (chicago_root / "chicago95.qss").read_text(encoding="utf-8")
    retro_dark = (chicago_root / "chicago95-dark.qss").read_text(encoding="utf-8")

    def url_targets(qss_text, placeholder, root):
        targets = set()
        for raw in re.findall(r"url\(([^)]+)\)", qss_text, flags=re.I):
            raw = raw.strip().strip("'\\\"")
            prefix = placeholder + "/"
            if raw.startswith(prefix):
                targets.add(root / raw[len(prefix):])
        return targets

    chicago_qss_targets = url_targets(
        retro_light, "__CHICAGO95_ROOT__", chicago_root
    )
    raleigh_qss_targets = url_targets(
        retro_dark, "__RALEIGH_ROOT__", raleigh_root
    )
    chicago_icon_targets = {
        chicago_root / "original/icons/actions/16/edit-find.png",
        chicago_root / "original/icons/actions/16/go-next.png",
        chicago_root / "original/icons/actions/16/go-previous.png",
    }

    for asset in chicago_qss_targets | chicago_icon_targets | raleigh_qss_targets:
        if not asset.is_file():
            fail(f"referenced Retro asset missing: {asset.relative_to(PROJECT_ROOT)}")

    allowed_chicago = {
        chicago_root / "ATTRIBUTION.md",
        chicago_root / "CHICAGO95-CREDITS",
        chicago_root / "chicago95.qss",
        chicago_root / "chicago95-dark.qss",
    } | chicago_qss_targets | chicago_icon_targets

    allowed_raleigh = {
        raleigh_root / "ATTRIBUTION.md",
        raleigh_root / "RALEIGH-LICENSE",
    } | raleigh_qss_targets

    actual_chicago = {path for path in chicago_root.rglob("*") if path.is_file()}
    actual_raleigh = {path for path in raleigh_root.rglob("*") if path.is_file()}

    extra_chicago = sorted(
        path.relative_to(chicago_root)
        for path in actual_chicago - allowed_chicago
    )
    extra_raleigh = sorted(
        path.relative_to(raleigh_root)
        for path in actual_raleigh - allowed_raleigh
    )
    if extra_chicago:
        fail(f"unused Chicago95 theme payload remains: {extra_chicago}")
    if extra_raleigh:
        fail(f"unused Raleigh theme payload remains: {extra_raleigh}")

    if len(chicago_qss_targets) != 19:
        fail(f"unexpected Chicago95 referenced-asset count: {len(chicago_qss_targets)}")
    if len(raleigh_qss_targets) != 5:
        fail(f"unexpected Raleigh referenced-asset count: {len(raleigh_qss_targets)}")

    if 'scrollbar_start = stylesheet.find("QScrollBar")' not in text:
        fail("Retro editor-canvas scrollbar suppression is missing")
    if "window.apply_editor_canvas_style()" not in text:
        fail("Retro toggle does not immediately rebuild editor scrollbar ownership")

    chicago_scrollbar_required = (
        "QScrollBar:vertical",
        "width: 16px",
        "margin: 16px 0px 16px 0px",
        'stepper-up.png',
        'stepper-down.png',
        'stepper-up-active.png',
        'stepper-down-active.png',
        "background: #c0c0c0",
        "background: #dfdfdf",
    )
    for marker in chicago_scrollbar_required:
        if marker not in retro_light:
            fail(f"Chicago95 source scrollbar marker missing: {marker}")

    raleigh_scrollbar_required = (
        "QScrollBar:vertical",
        "width: 16px",
        "margin: 16px 0px 16px 0px",
        "__RALEIGH_ROOT__/gtk-assets/dark/arrows/arrow-up.png",
        "__RALEIGH_ROOT__/gtk-assets/dark/arrows/arrow-down.png",
        "__RALEIGH_ROOT__/gtk-assets/dark/arrows/arrow-left.png",
        "__RALEIGH_ROOT__/gtk-assets/dark/arrows/arrow-right.png",
        "background: #232424",
        "border-top: 2px solid #434444",
        "border-right: 2px solid #000000",
        "background: #111111",
    )
    for marker in raleigh_scrollbar_required:
        if marker not in retro_dark:
            fail(f"Raleigh source scrollbar marker missing: {marker}")

    for chicago_indicator in (
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/checkbox-unchecked.png",
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/checkbox-checked.png",
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/checkbox-unchecked-insensitive.png",
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/checkbox-checked-insensitive.png",
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/radio-unselected.png",
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/radio-selected.png",
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/radio-unselected-insensitive.png",
        "__CHICAGO95_ROOT__/original/gtk-3.0/assets/radio-selected-insensitive.png",
    ):
        if chicago_indicator not in retro_dark:
            fail(f"dark Retro Chicago95 indicator missing: {chicago_indicator}")

    for forbidden_raleigh_indicator in (
        "gtk-assets/common/checks/",
        "gtk-assets/dark/checks/menu-item-check",
    ):
        if forbidden_raleigh_indicator in retro_dark:
            fail(f"dark Retro still uses Raleigh check artwork: {forbidden_raleigh_indicator}")

    for frame_marker in (
        "border-top: 2px solid #808080;",
        "border-left: 2px solid #808080;",
        "border-right: 2px solid #ffffff;",
        "border-bottom: 2px solid #ffffff;",
        "border-top: 2px solid #111111;",
        "border-left: 2px solid #111111;",
        "border-right: 2px solid #434444;",
        "border-bottom: 2px solid #434444;",
        "border-radius: 0px;",
    ):
        if frame_marker not in text:
            fail(f"Retro boxed editor frame marker missing: {frame_marker}")

    if text.count("QPlainTextEdit:focus {") < 2:
        fail("Retro focused editor-frame rules are missing")
    for focused_frame_marker in (
        "QPlainTextEdit,\nQPlainTextEdit:focus {",
        "border-top: 2px solid #808080;",
        "border-left: 2px solid #808080;",
        "border-right: 2px solid #ffffff;",
        "border-bottom: 2px solid #ffffff;",
        "border-top: 2px solid #111111;",
        "border-left: 2px solid #111111;",
        "border-right: 2px solid #434444;",
        "border-bottom: 2px solid #434444;",
    ):
        if focused_frame_marker not in text:
            fail(f"Retro focused frame persistence marker missing: {focused_frame_marker}")

    if "def restore_original_window_appearance(window):" not in text:
        fail("window-scoped host appearance helper is missing")

    retro_start = text.find("def apply_retro_theme(")
    retro_end = text.find("\ndef apply_kernel_modules_theme(", retro_start)
    retro_block = text[retro_start:retro_end]
    kernel_start = retro_end + 1
    kernel_end = text.find("\n\nclass LineNumberArea", kernel_start)
    kernel_block = text[kernel_start:kernel_end]

    for marker in (
        "window.setStyle(fusion_style)",
        "window.setPalette(palette)",
        "window.setFont(retro_font)",
        "window.setStyleSheet(stylesheet)",
    ):
        if marker not in retro_block:
            fail(f"Retro theme is not window-scoped: {marker}")
    if "window.setStyleSheet(stylesheet)" not in kernel_block:
        fail("Kernel Modules theme is not window-scoped")

    for name, block in (("Retro", retro_block), ("Kernel", kernel_block)):
        for forbidden in (
            "application.setStyleSheet(",
            "application.setPalette(",
            "application.setFont(",
            "application.setStyle(",
        ):
            if forbidden in block:
                fail(f"{name} shell still mutates QApplication: {forbidden}")

    constructor_start = text.find("class Nuxpad(QMainWindow):")
    constructor_end = text.find("    # ---------- Preferences ----------", constructor_start)
    constructor_block = text[constructor_start:constructor_end]
    if "apply_retro_theme(\n                    self," not in constructor_block:
        fail("constructor does not apply Retro to the Nuxpad window")
    if "apply_kernel_modules_theme(\n                    self," not in constructor_block:
        fail("constructor does not apply Kernel theme to the Nuxpad window")

    if "application.topLevelWidgets()" in text:
        fail("x3.11 live-widget freezing mechanism remains")
    if "--nuxpad-native-dialog-helper" in text:
        fail("x3.12 helper-process dialog mechanism remains")

    set_theme_start = text.find("    def set_application_theme(self, theme):")
    set_theme_end = text.find("    def toggle_retro_theme(", set_theme_start)
    set_theme_block = text[set_theme_start:set_theme_end]
    if "window.apply_selected_shell_theme()" in set_theme_block:
        fail("Dark/Light still repolishes synchronously inside the Theme menu")
    if "self._queue_shell_theme_apply()" not in set_theme_block:
        fail("Dark/Light does not queue the safe post-menu theme apply")

    toggle_start = text.find("    def toggle_retro_theme(self, checked):")
    toggle_end = text.find("    def apply_selected_shell_theme(", toggle_start)
    toggle_block = text[toggle_start:toggle_end]
    if "window.apply_selected_shell_theme()" in toggle_block:
        fail("Chicago95 toggle still repolishes synchronously inside the Theme menu")
    if "self._queue_shell_theme_apply()" not in toggle_block:
        fail("Chicago95 toggle does not queue the safe post-menu theme apply")

    queued_start = text.find("    def _queue_shell_theme_apply(self):")
    queued_end = text.find("    def refresh_shell_theme_state(", queued_start)
    queued_block = text[queued_start:queued_end]
    for marker in (
        "QTimer.singleShot(0, self._apply_queued_shell_theme)",
        "QApplication.activePopupWidget()",
        "isinstance(popup, QMenu)",
        "QTimer.singleShot(10, self._apply_queued_shell_theme)",
        "window.apply_selected_shell_theme()",
    ):
        if marker not in queued_block:
            fail(f"safe deferred theme-switch marker missing: {marker}")

    restore_start = text.find("def restore_original_window_appearance(window):")
    restore_end = text.find("\ndef apply_retro_theme(", restore_start)
    restore_block = text[restore_start:restore_end]
    if "host_style = application.style()" not in restore_block:
        fail("host window restore does not reuse QApplication-owned QStyle")
    if "QStyleFactory.create(str(original_style))" in restore_block:
        fail("host window restore still creates a transient QStyle")

    retro_start = text.find("def apply_retro_theme(")
    retro_end = text.find("\ndef apply_kernel_modules_theme(", retro_start)
    retro_block = text[retro_start:retro_end]
    for marker in (
        'getattr(window, "_nuxpad_retro_style", None)',
        'window._nuxpad_retro_style = fusion_style',
        "window.setStyle(fusion_style)",
    ):
        if marker not in retro_block:
            fail(f"retained Retro QStyle marker missing: {marker}")

    about_link_start = text.find("    def apply_about_link_palette(self):")
    about_link_end = text.find("    def show_about_dialog(self):", about_link_start)
    about_link_block = text[about_link_start:about_link_end]
    for marker in (
        '"#0000ff"',
        '"#7777ff"',
        'link_style = f"color:{link_hex};"',
        'style="{link_style}"',
        "QPalette.ColorRole.Link, link_colour",
        "QPalette.ColorRole.LinkVisited, link_colour",
    ):
        if marker not in about_link_block:
            fail(f"deterministic About link marker missing: {marker}")

    if 'details = QLabel(dialog)' not in text:
        fail("About details label is not populated through the authoritative renderer")
    if '<a href="https://github.com/brunonlinespace/nuxpad">' in text:
        fail("unstyled About repository anchor remains")
    if 'Copyright © 2026 <a href="https://github.com/brunonlinespace/">' in text:
        fail("unstyled About author anchor remains")
    if 'Themes: <a href="https://github.com/grassmunk/chicago95">' in text:
        fail("unstyled About theme anchor remains")


    view_start = text.find("    def make_view_menu(self):")
    view_end = text.find("    def open_external_url", view_start)
    view_block = text[view_start:view_end]
    for group_marker in (
        "self.layout_group = QActionGroup(self)",
        "self.layout_group.setExclusive(True)",
        "self.drop_behaviour_group = QActionGroup(self)",
        "self.drop_behaviour_group.setExclusive(True)",
        "self.application_theme_group = QActionGroup(self)",
        "self.application_theme_group.setExclusive(True)",
    ):
        if group_marker not in view_block:
            fail(f"radio-selector action group missing: {group_marker}")
    if "self.layout_group.addAction(action)" not in view_block:
        fail("Layout actions are not in the exclusive radio group")
    if "self.drop_behaviour_group.addAction(action)" not in view_block:
        fail("Drag-and-Drop actions are not in the exclusive radio group")
    if "self.application_theme_group.addAction(action)" not in view_block:
        fail("Dark/Light actions are not in the exclusive radio group")
    if "self.retro_theme_action" not in view_block or "self.application_theme_group.addAction(self.retro_theme_action)" in view_block:
        fail("Chicago95/Raleigh must remain an independent checkmark toggle")

    chicago_light = (PROGRAM_ROOT / "assets/themes/chicago95/chicago95.qss").read_text(encoding="utf-8")
    chicago_dark = (PROGRAM_ROOT / "assets/themes/chicago95/chicago95-dark.qss").read_text(encoding="utf-8")
    for marker in (
        "QMenu::indicator:non-exclusive:checked",
        "QMenu::indicator:exclusive:unchecked",
        "QMenu::indicator:exclusive:checked",
        "radio-unselected.png",
        "radio-selected.png",
    ):
        if marker not in chicago_light:
            fail(f"Chicago95 radio-menu styling missing: {marker}")
        if marker not in chicago_dark:
            fail(f"Raleigh Dark Chicago95-radio styling missing: {marker}")
    if "__RALEIGH_ROOT__/gtk-assets/dark/checks/menu-item-radio" in chicago_dark:
        fail("Raleigh Dark still uses Raleigh menu-radio artwork")
    if (PROGRAM_ROOT / "assets/themes/raleigh-dark/gtk-assets/dark/checks").exists():
        fail("obsolete Raleigh menu-radio assets remain")

    root_readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    for stale in (
        "https://github.com/brunonlinespace/nuxpad.py",
        "View → Behaviour",
        "RC5.1",
        "Current release-candidate targets",
        "Linux AppImage-only **Dark / Light** Breeze-inspired styling.",
    ):
        if stale in root_readme:
            fail(f"stale root README content remains: {stale}")
    for required_readme in (
        "nuxpad2/assets/icons/nuxpad-about.png",
        "○ **Dark** and ○ **Light** are mutually exclusive theme variants.",
        "✓ **Chicago95/Raleigh** is a checkmark",
        "**Layout** — mutually exclusive radio choices",
        "**Drag-and-Drop** — mutually exclusive radio choices",
        "./nuxpad2/packaging/fedora/build-appimage.sh",
        "python3 main.py",
        "## Current supported build targets",
    ):
        if required_readme not in root_readme:
            fail(f"root README current-contract marker missing: {required_readme}")

    # 2.2.8 requested selector/readme corrections.
    view_start = text.find("    def make_view_menu(self):")
    view_end = text.find("    def open_external_url", view_start)
    view_block = text[view_start:view_end]
    for group_name in (
        "self.layout_group",
        "self.drop_behaviour_group",
        "self.application_theme_group",
    ):
        policy = (
            group_name
            + ".setExclusionPolicy(\n"
            + "            QActionGroup.ExclusionPolicy.Exclusive\n"
            + "        )"
        )
        if policy not in view_block:
            fail(f"explicit Qt exclusive policy missing: {group_name}")

    for modern_theme in (
        PROGRAM_ROOT / "assets/themes/kernel-modules-dark.qss",
        PROGRAM_ROOT / "assets/themes/kernel-modules-light.qss",
    ):
        if "QMenu::indicator" in modern_theme.read_text(encoding="utf-8"):
            fail(f"modern style invents menu indicator artwork: {modern_theme.name}")

    root_readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    appearance_start = root_readme.find("## Appearance")
    appearance_end = root_readme.find("\n## ", appearance_start + 3)
    appearance = root_readme[
        appearance_start:appearance_end if appearance_end > appearance_start else len(root_readme)
    ]
    for marker in (
        "modern LinSpectacles style",
        "| Off | Dark | LinSpectacles Dark |",
        "| Off | Light | LinSpectacles Light |",
        "[Chicago95](https://github.com/grassmunk/chicago95)",
        "[Raleigh](https://github.com/thesquash/gtk-theme-raleigh)",
    ):
        if marker not in appearance:
            fail(f"README Appearance correction missing: {marker}")
    if "Kernel Modules" in appearance:
        fail("README Appearance still uses Kernel Modules naming")

    # 2.2.8 focused About-dialog contract.
    help_start = text.find("    def make_help_menu(self):")
    help_end = text.find("    def bind_shortcuts(self):", help_start)
    help_block = text[help_start:help_end]
    if 'menu, "About Nuxpad 2", self.show_about_dialog' not in help_block:
        fail("Help menu About entry is not labelled About Nuxpad 2")

    about_start = text.find("    def show_about_dialog(self):")
    about_end = text.find("    # ---------- Files ----------", about_start)
    about_block = text[about_start:about_end]
    if 'dialog.setWindowTitle(f"About — {APP_NAME}")' not in about_block:
        fail("About titlebar does not follow 'About — AppName'")
    if "dialog.setMinimumSize(640, 480)" not in about_block:
        fail("About minimum size is not 640x480")
    if "dialog.resize(640, 480)" not in about_block:
        fail("About default size is not 640x480")
    if "dialog.setMinimumWidth(390)" in about_block:
        fail("old undersized About width-only geometry remains")

    main_text = (PROJECT_ROOT / "main.py").read_text(encoding="utf-8")
    if "from nuxpad2.source.nuxpad import main" not in main_text:
        fail("portable main.py does not delegate to canonical Nuxpad source")


def check_packaging() -> None:
    builder = (PROGRAM_ROOT / "packaging/fedora/build-appimage.sh").read_text(encoding="utf-8")
    for fragment in [
        'APP_VERSION="2.2.8"',
        'OUTPUT_STEM="Nuxpad"',
        "Do not run the Nuxpad AppImage builder with sudo/root.",
        "Validated for Fedora 43/44.",
        '"$VENV/bin/python" -m pip check',
        "run_gui_smoke_test \"final AppImage\"",
        "run_version_smoke_test \"final AppImage\"",
        "APPIMAGETOOL_SHA256",
        "Qt PrintSupport was not bundled.",
        'BUILD_ROOT="${BUILD_ROOT:-$PROGRAM_ROOT/build/',
    ]:
        if fragment not in builder:
            fail(f"builder contract missing: {fragment}")
    if re.search(r"(?m)^\s*(sudo|dnf|pkexec|su)(?:\s|$)", builder):
        fail("builder contains privilege-elevation/host-package-install command")
    if 'install -m 0644 "$PROJECT_ROOT/README.md" "$APPDIR/usr/share/doc/nuxpad/README.md"' not in builder:
        fail("AppImage does not package the source-root README as Documentation")

    spec_text = (PROGRAM_ROOT / "packaging/pyinstaller/nuxpad.spec").read_text(encoding="utf-8")
    if '(str(project_root / "README.md"), "."),' not in spec_text:
        fail("PyInstaller does not bundle the source-root README")
    if '(str(package_root / "docs" / "README.md"), "."),' in spec_text:
        fail("PyInstaller still substitutes the internal README for Documentation")


    build_requirements = (PROGRAM_ROOT / "packaging/pyinstaller/build-requirements.txt").read_text(encoding="utf-8")
    if "\\n" in build_requirements:
        fail("build requirements contains a literal \\n escape instead of a real line break")
    build_lines = [
        line.strip() for line in build_requirements.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if build_lines != ["PyInstaller>=6.21,<7"]:
        fail(f"unexpected PyInstaller build requirements: {build_lines!r}")

    desktop = (PROGRAM_ROOT / "packaging/appimage/io.github.brunonlinespace.nuxpad.desktop").read_text(encoding="utf-8")
    for line in [
        "Name=Nuxpad 2",
        "Exec=nuxpad %F",
        "Icon=nuxpad",
        "MimeType=text/plain;text/x-log;",
    ]:
        if line not in desktop:
            fail(f"desktop metadata missing: {line}")

    meta = ET.parse(PROGRAM_ROOT / "packaging/appimage/io.github.brunonlinespace.nuxpad.metainfo.xml").getroot()
    if (meta.findtext("id") or "").strip() != "io.github.brunonlinespace.nuxpad":
        fail("AppStream ID mismatch")
    developer = meta.find("developer[@id='io.github.brunonlinespace']")
    if developer is None or (developer.findtext("name") or "").strip() != "Bruno Machado":
        fail("AppStream developer metadata missing")
    releases = meta.findall("./releases/release")
    if len(releases) != 1 or releases[0].attrib.get("version") != EXPECTED_VERSION:
        fail("AppStream release feed must contain current release only")
    if releases[0].attrib.get("date") != "2026-11-26":
        fail("AppStream current release date is missing or incorrect")
    urls = {node.attrib.get("type"): (node.text or "").strip() for node in meta.findall("url")}
    if urls.get("homepage") != "https://github.com/brunonlinespace/nuxpad":
        fail("AppStream homepage URL mismatch")
    if urls.get("bugtracker") != "https://github.com/brunonlinespace/nuxpad/issues":
        fail("AppStream bugtracker URL mismatch")
    description = (meta.findtext("./description/p") or "").strip()
    if len(description) < 100:
        fail("AppStream first description paragraph is too short")

    windows = (PROGRAM_ROOT / "windows/build-windows-portable.ps1").read_text(encoding="utf-8")
    if '$Version = "2.2.8"' not in windows:
        fail("Windows builder version mismatch")
    if 'Join-Path $ProjectRoot "main.py"' not in windows:
        fail("Windows builder is not using portable main.py")
    if 'Copy-Item -LiteralPath (Join-Path $ProjectRoot "README.md")' not in windows:
        fail("Windows portable package does not include the source-root README")


def check_manifest() -> None:
    expected = read_manifest()
    actual = inventory()
    missing = sorted(set(actual) - set(expected))
    stale = sorted(set(expected) - set(actual))
    if missing or stale:
        fail(f"source manifest inventory mismatch: missing={missing!r}, stale={stale!r}")
    bad = [path for path in sorted(actual) if actual[path] != expected[path]]
    if bad:
        fail(f"source manifest checksum mismatch: {bad!r}")


def main() -> int:
    check_structure()
    check_identity()
    check_source()
    check_packaging()
    check_manifest()
    print(f"PASS: Nuxpad 2 {EXPECTED_VERSION} source release gate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
