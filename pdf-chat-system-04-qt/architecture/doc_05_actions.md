# Doc 05 — Actions & Action Bundle

## Purpose

- Implement application workflows.
- Coordinate state changes (via the State Controller) and external work (via Gateways).
- Return results to Event Handlers; perform no UI work.

---

## Directory Structure

```text
desktop/
├── actions/
│   ├── __init__.py
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── send_message_action.py    # SendMessageAction
│   │   └── clear_chat_action.py      # ClearChatAction
│   └── document/
│       ├── __init__.py
│       └── upload_document_action.py # UploadDocumentAction
└── action_bundles/
    ├── __init__.py
    └── action_bundle.py              # ActionBundle (single, holds all actions)
```

---

## Implementation

- Every action is constructed with `(state_controller, gateways)` and exposes a single `execute(...)`.
- **`UploadDocumentAction.execute(file_path) -> PDFDocument`**
  - Calls `gateways.pdf.load_document` → stores the document in state → clears the chat (fresh conversation for the new PDF) → returns the `PDFDocument`.
- **`SendMessageAction.execute(user_text) -> tuple[ChatMessage, ChatMessage]`**
  - Sets `is_processing` true (reset in a `finally`).
  - Reads the current document and history from state.
  - Builds the provider message list: a system prompt (with the PDF text as context) + prior history + the new user turn. This is where `ChatMessage → dict` conversion happens.
  - Calls `gateways.chat.get_reply`.
  - Commits **both** the user and assistant turns to state **only after a successful reply** (atomic — a failed call leaves state unchanged).
  - Returns `(user_message, assistant_message)`.
- **`ClearChatAction.execute() -> None`**
  - Resets the session: clears the chat **and** removes the active document.
- **`ActionBundle`** — single frozen dataclass holding `send_message`, `clear_chat`, `upload_document`. Built by the Main Controller, passed to Event Handlers.

## Typical Flow

```text
Event Handler → Action → (read State) → Gateway → Core → (write State) → return to Event Handler
```

---

## Rules

- Organise actions by business/domain topic; one action represents one workflow.
- Actions are the only layer that reads/writes State (through the State Controller) and calls Gateways.
- Actions may access the State Controller and the Gateway Bundle; nothing else.
- Actions must not access UI, controllers, Event Handlers, or perform widget work.
- Actions are synchronous and UI-agnostic; threading (if any) is decided in the Event Handler, not here.
- Failures are raised, not swallowed; state is left consistent (commit only on success). Event Handlers handle errors.
- Provider message shaping (`ChatMessage → dict`, system prompt) belongs in the Action, not in the model or the gateway.
