# Doc 02 — UI Layer

## Purpose

- Render the interface, capture user interaction, and display data.
- Stay independent of business logic; depend on nothing below it except through injected callbacks.
- Never import or name Core models; consume primitives only.

---

## Directory Structure

```text
ui/
├── __init__.py
├── screen_manager.py       # composition root: builds ONE screen, returns UIBundle
├── main_window.py          # QMainWindow shell, single central widget
├── ui_bundle.py            # UIBundle — bundles the component controllers
├── style_manager.py        # loads + applies a .qss theme to the whole app
├── components/             # dumb, reusable components (one dir each, + widgets/)
│   ├── toolbar/            # toolbar_component + widgets (upload, filename, clear, theme combo)
│   ├── chat_area/          # chat_area_component + widgets (placeholder, message bubble)
│   ├── input_bar/          # input_bar_component + widgets (text input, send button)
│   ├── status_bar/         # status_bar_component
│   └── file_picker/        # file_picker (non-visual dialog launcher)
├── controllers/            # one controller per component (5)
├── pages/
│   └── main_page.py        # assembles components into the screen, returns UIBundle
└── styles/                 # 10 .qss themes + README
```

---

## Implementation — Components

- A component is a dumb renderer built in three named steps: `_create_widgets()`, `_create_layout()`, `_connect_signals()`.
- Leaf widgets self-configure in `_setup()` and set an `objectName` for QSS targeting.
- Components emit external signals on interaction (e.g. `upload_clicked`, `send_clicked(str)`, `theme_changed(str)`, `dismissed`, `pdf_selected(str)`).
- Components expose public operations called by their controller (e.g. `add_message`, `set_filename`, `show_error`).
- The chat placeholder hides on the first message and reappears on clear.

## Implementation — Component Controllers

- One controller per component; injected with its component.
- Provide `bind_*` methods (one per component signal) and operation methods (one task each).
- Consume **primitives only** — no Core models, no Core imports.

## Implementation — Page

- `MainPage` creates the components and their controllers, lays them out (toolbar → status bar → chat area → input bar; file picker is non-visual), and exposes `get_bundle() -> UIBundle`.

## Implementation — Styling

- `StyleManager.apply_theme(filename)` loads a file from `ui/styles/` and applies it globally via `QApplication.setStyleSheet`.
- 10 themes; the default (`theme_01_slate_indigo.qss`) is applied at startup by the Main Controller.
- Components carry no inline styles; all appearance is QSS-driven via object names / class selectors.

---

## Rules

- One controller per component; components stay dumb and passive.
- Components communicate only through signals; components never talk to each other, and controllers never talk to each other.
- The UI layer contains no business logic and never accesses State or Core.
- The UI layer never imports or names Core models; controllers consume primitives (or UI-local view types) only.
- Component appearance is controlled by QSS, not inline styles.
- `ui/` owns all window/page/component wiring; the Main Controller only receives the `UIBundle` and binds handlers to it.
