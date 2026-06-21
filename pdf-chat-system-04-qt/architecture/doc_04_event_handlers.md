# Doc 04 — Event Handlers

## Purpose

- Respond to UI events.
- Coordinate the flow between the UI (component controllers) and the Action layer.
- Translate Core models returned by Actions into primitives before updating the UI.

---

## Directory Structure

```text
desktop/event_handlers/
├── __init__.py
├── toolbar_event_handler.py        # upload, clear, theme
├── input_bar_event_handler.py      # send
├── status_bar_event_handler.py     # dismiss
└── file_picker_event_handler.py    # pdf_selected, dialog_canceled
```

Handlers are organised by the component that emits the event. (`ChatAreaComponent` emits nothing, so it has no handler; it is only updated through its controller.)

---

## Implementation

- Constructors receive the **Action Bundle** and the **component controllers** they need (and, for the toolbar, the **StyleManager**). Controllers are injected as plain objects — never imported.
- **`InputBarEventHandler(actions, chat_area_controller, input_bar_controller)`**
  - `on_send_clicked(text)`: disable input → `actions.send_message.execute(text)` → unpack both `ChatMessage`s to `(role, content)` and add to chat → clear the box on success. On error, show an **error bubble in the chat area**. Always re-enable input in a `finally`.
- **`ToolbarEventHandler(actions, style_manager, file_picker_controller, toolbar_controller, chat_area_controller, input_bar_controller, status_bar_controller)`**
  - `on_upload_clicked()`: opens the file dialog via the file-picker controller.
  - `on_clear_clicked()`: `actions.clear_chat.execute()` → reset chat area, toolbar, input bar, status bar.
  - `on_theme_changed(filename)`: `style_manager.apply_theme(filename)`.
- **`FilePickerEventHandler(actions, toolbar_controller, input_bar_controller, chat_area_controller, status_bar_controller)`**
  - `on_pdf_selected(path)`: `actions.upload_document.execute(path)` → unpack `PDFDocument.filename` to the toolbar, enable input, clear chat. On error, show the **status-bar banner**.
  - `on_dialog_canceled()`: no-op.
- **`StatusBarEventHandler(status_bar_controller)`**
  - `on_dismissed()`: hide the banner.

## Error Surfaces

- Chat / LLM failures → inline error bubble in the chat area.
- PDF-load failures → dismissible status-bar banner.

## Typical Flow

```text
Component signal → Event Handler method → Action → (Core model result) → unpack to primitives → Component Controller → UI
```

---

## Rules

- Organise handlers by the emitting component; one handler may process several events from that component.
- Handlers may access component controllers (injected) and the Action Bundle (and StyleManager for the toolbar).
- Handlers must not import the UI layer, access Core, or touch State directly.
- All UI updates go through component controllers; all state/business changes go through Actions.
- Handlers unpack Core models into primitives before calling controllers (UI never sees `ChatMessage`/`PDFDocument`).
- Handlers catch Action failures and route them to the correct error surface.
- The Main Controller (not the handler) connects component signals to handler methods.
