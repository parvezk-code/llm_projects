# ChatPDF AI Agent — Core Layer Design Document

**`core/` Directory — Architecture & Conventions** — Draft, Not Yet Finalized

## 1. Overview

This document is reserved for the design of the `core/` package of the ChatPDF application — the business logic layer responsible for PDF processing, embeddings, retrieval, and LLM communication.

Unlike ui_design.md, the contents of this document have **not** yet been through a finalization discussion. It currently contains only the early sketch proposed during initial project structuring, kept here as a starting point for a future design session.

## 2. Layer Purpose (Agreed, Not Yet Detailed)

- `core/` contains zero PyQt6 imports and has no awareness of any UI widget, controller, or page.
- `core/` is called only from `controllers/` (see ui_design.md, Section 6) — never directly from `components/` or `pages/`. (In the `api_server/` deployment mode, `core/` is also called from server route handlers — to be detailed in api_design.md once that document exists.)
- `core/` should be fully testable and runnable independent of the UI (e.g. from a script or a test suite).

## 3. Early Sketch (Not Finalized — For Reference Only)

```
core/
├── __init__.py
├── pdf_processor.py    extracts text from uploaded PDFs
├── text_chunker.py     splits extracted text into chunks
├── embeddings.py       generates embeddings for text chunks
├── vector_store.py     stores/searches embeddings (vector index)
├── llm_client.py       talks to the LLM API
├── chat_engine.py      ties retrieval + generation into the
│                        "ask a question, get an answer" flow
└── models.py           shared data classes (e.g. ChatMessage,
                         Document) used by both ui/ and core/
```

## 4. Open Items (Not Yet Finalized)

- Whether the above file breakdown is correct/complete, or needs restructuring (e.g. splitting into sub-packages such as `core/pdf/`, `core/llm/`, `core/storage/`).
- Which vector store / embedding provider / LLM provider to use.
- Whether `models.py` should instead live in a shared location accessible to both `ui/` and `core/`, rather than inside `core/` itself.
- Error handling and logging conventions for this layer.
- How `chat_engine.py` exposes its API to `controllers/` (function calls, callbacks, async/await, signals, etc.).
- How `core/` is exposed to `api_server/` once that piece is built (likely direct function/class calls from FastAPI route handlers, but not yet decided).

This document will be updated once `core/` design is finalized in a dedicated session.