# Architecture Overview

## Goal

* Separate UI from business logic.
* Support local and remote execution.
* Keep modules loosely coupled.
* Make testing and maintenance easier.

---

## Directory Structure

```text

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
├── desktop/                        # Desktop application logic
|
├── desktop_local/                  # Local startup
|       |
|       └── main.py                 # Application orchestrator
|
└── desktop_remote/                 # Remote startup
        |
        └── main.py                 # Application orchestrator

```

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
