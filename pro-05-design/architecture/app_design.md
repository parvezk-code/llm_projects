# ChatPDF AI Agent — Application Design Document

**Top-Level Architecture** — Finalized as of June 17, 2026

## 1. Overview

This document records the top-level architecture decisions for the ChatPDF application, built using Python, PyQt6, and (planned) FastAPI. The application now supports two ways of running the desktop UI — using `core/` logic directly on the same machine, or using a remote server over HTTP — plus the server itself as a third deployable piece.

## 2. Document Map

This project uses four design documents, one per architectural concern (not one per folder — `desktop_local/` and `desktop_remote/` are thin composition roots and are documented in Section 5 of this file instead of getting their own document):

- **app_design.md** — this document. Top-level structure, deployment modes, decision log.
- **ui_design.md** — everything inside `ui/` (components, controllers, pages, styles, the binding convention).
- **core_design.md** — everything inside `core/`. Currently a draft — not yet finalized.
- **api_design.md** — `api_server/` and `api_client/` together (the request/response contract between them). Not yet created — to be written once `api_server/` and `api_client/` are actually being built.

## 3. Top-Level Structure

```
app/
├── __init__.py
├── ui/                  (see ui_design.md)
├── core/                (see core_design.md)
├── api_server/          (see api_design.md - not yet created)
│   └── main.py            entry point, runs the FastAPI server
├── api_client/          (see api_design.md - not yet created)
├── desktop_local/
│   └── main.py            entry point, launches PyQt6 app wired to core/ directly
└── desktop_remote/
    └── main.py            entry point, launches PyQt6 app wired to api_client/
```

> **Note:** There is no project-root `main.py`. An earlier version of this project's structure proposed one root-level `main.py` as the single entry point; that is now superseded, since there are three independent ways to launch part of this application, each requiring a different backend to be wired up before `ui/` is shown.

## 4. Architectural Rationale

Each folder under `app/` plays exactly one of these roles:

- **`core/`** is the application's business logic, with zero awareness of PyQt6 or HTTP. It is the one piece every other folder ultimately depends on or exposes.
- **`ui/`** is the PyQt6 presentation layer. It is reusable across both desktop modes because it never imports `core/` or `api_client/` directly — see ui_design.md, Section 6, for how it receives its backend instead.
- **`api_server/`** exposes `core/` over HTTP, so a `desktop_remote/` instance (or any future client) does not need `core/`'s dependencies installed locally.
- **`api_client/`** is what `desktop_remote/` uses in place of `core/` — it makes HTTP calls to `api_server/` and returns results in the same shape a controller would expect from `core/` directly.
- **`desktop_local/`** and **`desktop_remote/`** are composition roots. Each one's `main.py` decides which backend object to construct (a `core/` object, or an `api_client/` object), then hands that object to `ui/` when building the main window.

## 5. Deployment Modes

| Mode | Entry Point | Depends On |
|---|---|---|
| desktop_local | `desktop_local/main.py` | `ui/`, `core/` (direct in-process calls) |
| desktop_remote | `desktop_remote/main.py` | `ui/`, `api_client/` (HTTP calls to a running `api_server/`) |
| api_server | `api_server/main.py` | `core/` (wraps it as HTTP endpoints) |

## 6. Key Design Decisions Log

- `app/` expanded from a 2-folder split (`ui/`, `core/`) to a 6-folder split: `ui/`, `core/`, `api_server/`, `api_client/`, `desktop_local/`, `desktop_remote/`.
- No project-root `main.py`. Each of `api_server/`, `desktop_local/`, and `desktop_remote/` has its own `main.py` as its entry point.
- A formal interface/Protocol describing the backend object that `ui/` controllers call (e.g. `ask_question`, `load_pdf`) has been deliberately deferred. For now this contract is enforced only by naming convention between `core/`'s objects and `api_client/`'s objects — see ui_design.md, Section 6, for detail.
- A shared folder for API request/response schemas (between `api_server/` and `api_client/`) has also been deliberately deferred, for the same reason — there is not yet enough concrete code on either side to know the right shape.
- Four design documents total — see Section 2 of this file.

## 7. Open Items (Not Yet Finalized)

- Formal interface/Protocol for the backend object injected into `ui/` (deferred — see decision log).
- Shared schema folder for `api_server/` ↔ `api_client/` requests and responses (deferred — see decision log).
- Internal breakdown of `core/` — see core_design.md.
- api_design.md has not been written yet — pending once `api_server/` and `api_client/` are actually being built.
- `data/`, `resources/`, `tests/`, `docs/` folders proposed at the very start of the project have not been broken down in detail yet.
- `requirements.txt` contents (exact dependency list) not yet decided.