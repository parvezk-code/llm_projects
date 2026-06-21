# State

## Purpose

Store application data.

State represents the current state of the application and contains no workflow logic.

---

## Directory Structure

```text id="f9a7ks"
state/
├── app_state.py            # Application-wide state
├── chat_state.py           # Chat-related state
└── document_state.py       # Document-related state

state_controller/
└── state_controller.py     # Single access point to state
```

---

## State Object Responsibilities

### Responsibilities

* Store data.
* Expose data fields.
* Represent current application state.

### Must Not

* Contain business logic.
* Contain workflow logic.
* Access Core.
* Access Gateways.
* Access UI.

---

## State Controller Responsibilities

### Responsibilities

* Provide access to state objects.
* Read state.
* Update state.
* Encapsulate state operations.
* Act as the single access point to state.

### May Access

* State Objects

---

### Must Not

* Access UI.
* Access Event Handlers.
* Access Core.
* Access Gateways.
* Implement business logic.

---

## Typical Flow

```text id="ebn6mz"
Action
    ↓
State Controller
    ↓
State Object
```

---

## Design Rules

* State stores data only.
* State objects remain simple.
* All state access goes through State Controller.
* Event Handlers never access State directly.
* UI never accesses State directly.
* Actions own state changes.
* State may import core/models/ (passive dataclasses) for storage and type annotations. 
* State must never depend on Core logic (services, processors, validators) or on Actions.
