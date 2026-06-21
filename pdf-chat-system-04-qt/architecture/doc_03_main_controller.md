# Doc 03 — Main Controller

## Purpose

- Act as the single composition root and orchestrator of the application.
- Create and wire State, Actions, UI, StyleManager, and Event Handlers.
- Receive ready-made Gateways from the launcher; never build them or decide the mode.

---

## Directory Structure

```text
desktop/
└── main_controller.py     # MainController
```

---

## Implementation

- **`MainController(gateways, screen="main")`** — receives the `GatewayBundle`; holds a `DEFAULT_THEME` constant (`theme_01_slate_indigo.qss`).
- **`start()`** runs the startup sequence, one task per step:
  1. `_create_state()` — build `AppState` and `StateController`.
  2. `_create_actions()` — build the three actions and pack them into the single `ActionBundle`.
  3. `_create_ui()` — build the UI via `ScreenManager(screen).build()`, obtaining the `UIBundle`.
  4. `_create_style()` — build the `StyleManager`.
  5. `_create_event_handlers()` — build the four handlers, injecting controllers (from the `UIBundle`), the `ActionBundle`, and the `StyleManager`.
  6. `_wire_events()` — bind every component signal to a handler method.
  7. `_apply_default_theme()` — apply `DEFAULT_THEME`.
  8. `_show()` — show the window via the ScreenManager.

## Event Wiring (performed here)

```text
toolbar.upload_requested   → ToolbarEventHandler.on_upload_clicked
toolbar.clear_clicked      → ToolbarEventHandler.on_clear_clicked
toolbar.theme_changed      → ToolbarEventHandler.on_theme_changed
input_bar.send_clicked     → InputBarEventHandler.on_send_clicked
status_bar.dismissed       → StatusBarEventHandler.on_dismissed
file_picker.pdf_selected   → FilePickerEventHandler.on_pdf_selected
file_picker.dialog_canceled→ FilePickerEventHandler.on_dialog_canceled
```

## Launcher Boundary

```text
desktop_local/  → builds LOCAL Gateways → constructs & starts MainController
```

The Main Controller only ever receives Gateways; it has no knowledge of which mode produced them.

---

## Rules

- Only one Main Controller exists per application; it is the composition root.
- It creates objects and wires dependencies; it holds no business logic.
- It must not access Core, mutate State, manipulate widgets directly, or contain event-handling logic.
- It must not build Gateway implementations or decide local-vs-remote mode.
- UI work is delegated to the ScreenManager and controllers; it never touches widgets itself.
