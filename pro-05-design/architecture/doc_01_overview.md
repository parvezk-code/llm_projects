# Architecture Overview

## Goal

* Separate UI from business logic.
* Support local and remote execution.
* Keep modules loosely coupled.
* Make testing and maintenance easier.

---

## Directory Structure

```

app/
|
├── ui/                             # User interface
|
├── core/                           # Business logic
|
├── api_server/                     # Exposes core through APIs
|
├── api_client/                     # Consumes remote APIs
|
├── desktop/                        # Desktop application logic (mode-agnostic)
|
├── desktop_local/                  # Local launcher: builds LOCAL Gateways, starts app
|
└── desktop_remote/                 # Remote launcher: builds REMOTE Gateways, starts app

```

> **Mode decision ownership.** Whether the app runs in local or remote mode
> is decided entirely by which launcher is run — `desktop_local/` or
> `desktop_remote/`. Each launcher builds the matching Gateway
> implementations (local: call Core directly; remote: call Core through
> `api_client/`) and hands them to `desktop/main_controller.py`, which acts
> as a pure orchestrator. Main Controller never knows or decides which mode
> it is in. Everything below Main Controller (Actions, Event Handlers,
> Core, State) is completely mode-agnostic.

---

## Dependency Direction

```
UI
 ↓
Event Handlers
 ↓
Actions
 ↓
State Controller + Gateways
 ↓
Core
```

* Dependencies flow downward only.
* Lower layers do not depend on higher layers.

---

## High-Level Flow

```text
User
 ↓
UI
 ↓
Event Handler
 ↓
Action
 ↓
Gateway
 ↓
Core
```

Response:

```text
Core
 ↓
Gateway
 ↓
Action
 ↓
Event Handler
 ↓
UI
```