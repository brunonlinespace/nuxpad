# Nuxpad 2.2.8 — merged modern + Retro theme experiment

x3.0 merges x2.6 with the Chicago95/Raleigh apparatus from x1.2.

## Default

Chicago95/Raleigh is OFF by default. View → Theme remains the single Dark / Light radio
selector.

With Retro OFF:

- Dark = Kernel Modules dark
- Light = dimmed Kernel Modules/Maqarony/Dolphin light from x2.6

## Retro

View → Theme → Chicago95/Raleigh is the final checkable option, separated from Dark/Light by a separator.

With Chicago95/Raleigh checked, the same View → Theme Dark/Light choice selects:

- Dark = Raleigh-derived dark Retro theme
- Light = Chicago95 light

There is no second Retro Dark/Light control.

Only Chicago95/Raleigh artwork actually referenced by Nuxpad is retained.
Retro also preserves x1.2's `MS Sans Serif` 11 pt program-font apparatus.
Turning Retro off restores the original system Qt style, palette and font before
the selected x2.6 shell is applied.

## Editor canvas

View → Dark Editor Canvas remains independent in all four shell combinations.
Display Font remains document-only. The line-number font remains the original
system UI font rather than the Retro program font.

## Native Open picker

The x2.6 native/un-themed Open picker path is retained.

## Scope

Only theme selection/apparatus is merged. File handling, encoding/BOM
preservation, saving, external-change protection, search, printing,
drag-and-drop and window lifetime are unchanged.

## x3.2 menu/help/symbols alignment

- View begins with Menu Only and Status Bar.
- Word Wrap, Line Numbers and Dark Editor follow, with the new shortcuts.
- Behaviour is renamed Drag-and-Drop with shorter option labels.
- Help now provides Documentation (F1), Keyboard Shortcuts, GitHub Repository,
  Raise an Issue, and About Nuxpad in the requested grouped order.
- About credits Chicago95 and Raleigh with upstream links.
- Symbols uses RiqatonyPad 2.0.0's centred modal chooser and full 40-symbol set.

## x3.4 theme asset purge

The theme payload is now reference-minimal.

- `themes/chicago95/` contains the two Nuxpad Qt QSS adaptations, attribution,
  Chicago95 credits, the 19 Chicago95 GTK artwork files referenced by the light
  QSS, and the three action icons Nuxpad actually requests.
- `themes/raleigh-dark/` is now a sibling of `themes/chicago95/`, because
  Gtk-Theme-Raleigh is a separate upstream project rather than part of
  Chicago95.
- Raleigh retains only its 15 referenced control assets plus attribution and
  the supplied LGPL-3.0 licence text.
- `chicago95-dark.qss` uses a separate `__RALEIGH_ROOT__` placeholder.
- Unreferenced upstream README, theme-index, GTK CSS and unused artwork/icon
  files are removed.

No theme behaviour, editor-canvas behaviour, or menu behaviour is changed.

## x3.5 Retro scrollbar restoration

Retro scrollbar ownership is restored to the original x1.2 source apparatus.

- `chicago95.qss` and `chicago95-dark.qss` are re-seeded directly from x1.2.
- Chicago95 Light therefore again uses the exact 16 px Windows-95-style
  steppers, active stepper artwork, `#c0c0c0` raised handles and `#dfdfdf`
  trough.
- Raleigh Dark again uses the exact x1.2 16 px geometry, Raleigh arrow artwork,
  `#232424` raised handles, `#434444` light edges, `#000000` dark edges and
  `#111111` trough.
- The only change to the x1.2 dark QSS is the path placeholder required by
  Raleigh's corrected sibling location: `__RALEIGH_ROOT__`.
- While Retro is active, the independent editor-canvas stylesheet no longer
  contributes QScrollBar rules, preventing it from overriding the Retro source
  scrollbar apparatus.
- Switching Retro on or off immediately reapplies the editor-canvas boundary.

Kernel Modules Dark/Light and the non-Retro editor scrollbars are unchanged.

## x3.6 Retro canvas framing and Chicago95 indicators

Retro restores the x1.2 inset/boxed editor frame as well as the x1.2
scrollbars.

- Chicago95 Light frame: 2 px `#808080` top/left and 2 px `#ffffff`
  right/bottom, square corners.
- Raleigh Dark frame: 2 px `#111111` top/left and 2 px `#434444`
  right/bottom, square corners.
- Dark Editor remains independent for canvas fill/text.
- Retro Dark uses Chicago95's 16 px checkbox/radio indicator assets and
  Chicago95 menu checkmark, matching Retro Light.
- Raleigh continues to provide its dark palette and arrow/scrollbar artwork.
- Raleigh check/radio/menu-check assets are no longer bundled because Nuxpad
  no longer references them.

Modern Kernel Modules themes are unchanged.

## x3.7 Retro editor-frame focus persistence

The x1.2 boxed Retro editor frame is now applied to both the normal and focused
`QPlainTextEdit` states.

This prevents the independent editor-canvas `QPlainTextEdit:focus` rule from
replacing the Retro 2 px inset frame when the user clicks into the document.

No colours, scrollbar assets, indicator assets, menu behaviour, or editor
canvas preference semantics are changed.

## x3.13 Path Inspector native-dialog architecture

x3.13 is built from x3.7 and adopts LinSpectacles Path Inspector 0.0.14 as the
dialog/style-scoping authority: style the top-level application window, never
`QApplication` or native choosers.

Kernel Modules and Chicago95/Raleigh shell styling are now owned by each
`Nuxpad` top-level window. The host `QApplication` remains untouched. Open,
Save As, Print/Print to File and Display Font are parentless external dialogs.

The x3.8-x3.12 dialog workarounds are not carried forward. Retro canvas,
scrollbars, Chicago95 indicators and document/save behaviour remain x3.7.

## x3.14 safe live theme switching + Light About links

x3.14 keeps the x3.13 Path Inspector window-scoped/native-dialog architecture.

Two focused corrections are made:

- theme actions no longer call `setStyleSheet()` / `setStyle()` while their
  `QMenu` is still executing; the selected state is stored immediately and the
  actual per-window shell repolish is queued until there is no active `QMenu`;
- the per-window Fusion style used by Chicago95/Raleigh is now strongly retained
  on the Nuxpad window because `QWidget.setStyle()` does not transfer ownership;
  host restoration reuses the QApplication-owned host style instead of creating
  a temporary QStyle;
- About-dialog links are explicitly standard blue (`#0000ff`) whenever Light is
  selected, including Chicago95 Light, and readable blue (`#7777ff`) in Dark;
  visited links use the same colour.

No native-dialog architecture, Retro assets, canvas, scrollbars, editor, save or
print behaviour is otherwise changed.

## x3.15 deterministic About hyperlink colours

About hyperlinks now carry their colour directly in each rich-text anchor:
Light/Chicago95 Light uses `#0000ff`; Dark/Raleigh Dark uses `#7777ff`.
`LinkVisited` is held to the same colour. No other behaviour changes.
