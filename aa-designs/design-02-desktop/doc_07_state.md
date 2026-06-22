# Doc 07 — State & State Controller (Generic)

## Purpose

- Store current application data in one place.
- Provide a single controlled access point for reading and writing it.
- Contain no workflow or business logic.

---

## Directory Structure

```text
desktop/
├── state/
│   └── app_state.py            # state object(s) — DATA ONLY
└── state_controller/
    └── state_controller.py     # the single access point — METHODS
```

Use one state object or several, but a single State Controller as the access layer.

---

## Responsibilities

- **State object** — holds data as plain fields and nothing else (no methods, no logic). May import domain models for type annotations.
- **State Controller** — receives the state object(s) by injection; the only object that touches state.
  - Exposes read methods (returning copies of mutable collections) and write methods.
  - Encapsulates all state operations.

## Typical Flow

```text
Action → State Controller → State Object
```

---

## Rules

- State stores data only; the state object has no methods and no logic.
- All state access goes through the State Controller.
- The State Controller holds no business or workflow logic.
- State and State Controller may import domain **models** (passive data) but never Core **logic**, Gateways, Actions, or UI.
- Only Actions mutate state; Event Handlers and UI never access state directly.
- Reads that expose mutable collections return copies.
