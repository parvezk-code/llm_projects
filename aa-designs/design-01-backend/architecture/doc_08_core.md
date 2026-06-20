# Core

## Purpose

Contain the application's business logic.

The Core implements domain rules and processing independent of UI, state management, and infrastructure.

---

## Directory Structure

```text id="9v4xdt"
core/
├── services/              # Business operations
├── models/                # Domain models
├── processors/            # Processing logic
├── validators/            # Validation rules
└── utils/                 # Core-only utilities
```

> The internal structure of `core/` may vary based on application needs.

---

## Responsibilities

* Implement business logic.
* Apply domain rules.
* Process data.
* Perform calculations.
* Validate business constraints.
* Return results.

---

## Typical Flow

```text id="9s1q6s"
Action
    ↓
Gateway
    ↓
Core
```

---

## May Access

* Internal Core modules.

---

## Must Not

* Access UI.
* Access Component Controllers.
* Access Event Handlers.
* Access State.
* Access Actions.
* Depend on desktop-specific code.

---

## Design Rules

* Core must be independent of UI.
* Core must be independent of application flow.
* Core should be reusable in local and remote modes.
* Business rules belong in Core.
* Workflow orchestration does not belong in Core.
* UI logic does not belong in Core.
