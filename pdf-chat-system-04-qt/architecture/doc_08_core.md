# Doc 08 — Core

## Purpose

- Hold the application's business logic and domain data.
- Stay independent of UI, application flow, state management, and infrastructure.
- Be reusable unchanged in local or remote mode.

---

## Directory Structure

```text
core/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── chat_message.py     # ChatMessage (+ Role)
│   └── pdf_document.py     # PDFDocument
└── services/
    ├── __init__.py
    ├── llm_service.py      # LLMService (OpenAI wrapper)
    └── pdf_service.py      # PDFService (PyMuPDF wrapper)
```

---

## Implementation — Models

- **`ChatMessage`** — frozen dataclass with `role: str` and `content: str`.
  - `Role` holds the two role strings in one place: `Role.USER = "user"`, `Role.ASSISTANT = "assistant"`.
  - Factory constructors: `ChatMessage.user(content)` and `ChatMessage.assistant(content)`.
  - Pure data: no `to_dict()` (the `ChatMessage → dict` conversion lives in the Action).
- **`PDFDocument`** — frozen dataclass with `filename`, `file_path`, `text`, `page_count`.

## Implementation — Services

- **`LLMService(api_key, model, temperature, max_tokens)`** — wraps the OpenAI client; `call(messages: list[dict]) -> str` returns the assistant reply.
- **`PDFService`** — wraps PyMuPDF (`fitz`); `extract_text(file_path: str) -> tuple[str, int]` returns `(full_text, page_count)`.

---

## Rules

- Core must not access UI, State, Actions, Gateways, or desktop-specific code.
- Models are passive: they store and represent data only; no workflow logic.
- Models are immutable (`frozen=True`); a change means a new instance.
- Services perform single, well-scoped operations and return plain values or domain models.
- Provider/library specifics (OpenAI, PyMuPDF) are confined to Core services.
- Core must be importable and usable identically in local and remote modes.
