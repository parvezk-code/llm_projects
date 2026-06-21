# Doc 06 — State & State Controller

## Purpose

- Store the current application data in one place.
- Provide a single, controlled access point for reading and writing that data.
- Contain no workflow or business logic.

---

## Directory Structure

```text
desktop/
├── state/
│   ├── __init__.py
│   └── app_state.py            # AppState — the single state object (DATA ONLY)
└── state_controller/
    ├── __init__.py
    └── state_controller.py     # StateController — the single access point (METHODS)
```

---

## Implementation — AppState (data only)

- A single `AppState` object holds all application data as plain fields:
  - `document: PDFDocument | None`
  - `messages: list[ChatMessage]`
  - `is_processing: bool`
- `AppState` has **no methods** — it is a pure data container.
- It imports `core/models` only for type annotations (dumb data types).

## Implementation — StateController (methods)

- Receives the `AppState` instance via constructor injection; it is the only object that touches `AppState`.
- Document: `set_document`, `get_document`, `has_document`, `clear_document`.
- Chat: `add_chat_message`, `get_chat_messages` (returns a **copy**), `remove_last_chat_message`, `is_chat_empty`, `clear_chat`.
- Processing: `set_processing`, `is_processing`.

---

## Rules

- State stores data only; the state object has no methods and no logic.
- All state access goes through the State Controller.
- The State Controller contains no business or workflow logic.
- State and State Controller may import `core/models` (passive data), but never Core **logic** (services/processors), Gateways, Actions, or UI.
- Only Actions mutate state (by calling State Controller methods); Event Handlers and UI never access state directly.
- Reads that expose mutable collections return copies, so callers cannot mutate internal state.
