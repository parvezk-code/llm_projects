# Doc 10 — UI Composition (ScreenManager, MainWindow, UIBundle, StyleManager)

## Purpose

- Define how the UI is assembled and handed to the Main Controller.
- Keep all window/page wiring inside `ui/`; the Main Controller only receives a `UIBundle` and asks for the window to be shown.

---

## Directory Structure

```text
ui/
├── screen_manager.py   # selects + builds ONE screen at startup, returns UIBundle
├── main_window.py      # QMainWindow shell with a single central widget
├── ui_bundle.py        # UIBundle — frozen bundle of component controllers
├── style_manager.py    # applies a .qss theme to the whole application
└── pages/
    └── main_page.py    # builds one screen, exposes get_bundle()
```

---

## Implementation

- **`ScreenManager(screen="main")`** — the UI composition root and the only UI object the Main Controller talks to.
  - `build() -> UIBundle`: selects the page class from a registry, builds the page once, sets it as the window's central widget, and returns the page's `UIBundle`.
  - `show()`: shows the window.
  - Holds a `_PAGES` registry mapping screen keys to Page classes.
- **`MainWindow`** — a `QMainWindow` shell; `set_page(widget)` sets the single central widget; title "Chat PDF", initial size 700×600. No components, no logic.
- **`MainPage`** — creates components + controllers, builds the layout, and exposes `get_bundle()`.
- **`UIBundle`** — frozen dataclass bundling the five component controllers: `toolbar`, `status_bar`, `chat_area`, `input_bar`, `file_picker`.
- **`StyleManager`** — loads a `.qss` from `ui/styles/` and applies it via `QApplication.setStyleSheet`.

## Screen Lifetime

- Exactly one screen is chosen and built at startup and lives for the whole process.
- There is no runtime screen switching; Event Handlers are wired to its controllers once.
- Multiple Page classes may exist (same components, different layout/look), but only one is instantiated per run.

## Startup Interaction

```text
MainController.start():
  ScreenManager.build() → UIBundle      # UI builds itself, returns controllers
  wire handlers to UIBundle controllers
  StyleManager.apply_theme(DEFAULT)
  ScreenManager.show()
```

---

## Rules

- `ui/` owns all window, page, and component wiring; the Main Controller never touches widgets, windows, or layouts.
- The ScreenManager owns the window and builds exactly one screen; it knows nothing about Event Handlers, Actions, Gateways, Core, or mode.
- The MainWindow is a dumb shell holding a single central widget.
- The `UIBundle` holds controllers (never raw components) and contains no logic.
- The UI layer is mode-agnostic and identical for local and remote launchers.
