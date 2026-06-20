# Event Handlers

## Purpose

Event Handlers respond to UI events.

They coordinate the flow between the UI layer and the Action layer.

---

## Directory Structure

```

event_handlers/
│
├── chat_area_event_handler.py                 # Events emitted by chat area
│
├── input_bar_event_handler.py                 # Events emitted by input bar
│
├── toolbar_event_handler.py                   # Events emitted by toolbar
│
└── status_bar_event_handler.py                # Events emitted by status bar

```

---

## Organization Rule

Event Handlers are organized by the component that emits the event.

```

Component
    ↓
Event Handler

```

Actions are organized by business/domain topics.

---

## Responsibilities

* Respond to UI events.
* Read data from Component Controllers.
* Call Actions.
* Receive results from Actions.
* Update UI through Component Controllers.
* Coordinate UI event flow.

---

## Typical Flow

```

Component Event
    ↓
Event Handler
    ↓
Action
    ↓
Event Handler
    ↓
Component Controller

```

---

## Core Model Translation Boundary

Event Handlers are the single translation point between Core domain models
and the UI. Actions return results to Event Handlers as Core models (e.g.
`ChatMessage`, `PDFDocument`). The Event Handler reads the fields it needs off
those models and passes **primitive values** (or UI-local view types) down to
Component Controllers.

Component Controllers and the UI layer never receive, name, or import Core
models. The Core model stops at the Event Handler.

```text

Action  ──returns──>  ChatMessage / PDFDocument   (Core model)
                             ↓
                       Event Handler   (reads .role, .content, .filename …)
                             ↓
                  Component Controller   (receives str / bool / primitives only)

```

**Rule:** The Event Handler unpacks; the Component Controller consumes
primitives. This keeps the UI layer free of any compile-time dependency on
Core, satisfying the dependency-direction rule (UI never depends on Core).

If a payload grows large enough that long primitive argument lists become
unwieldy, the Event Handler may map the Core model into a **UI-local view
object** — a dumb dataclass owned by the UI layer, not by Core. The boundary
rule is unchanged: no Core type crosses into the UI layer.

---

## May Access

* Component Controllers
* Action Bundles

---

## Must Not

* Contain business logic.
* Access Core directly.
* Access State directly.
* Modify State directly.
* Access Gateways directly.
* Communicate with other Event Handlers directly.

---

## Design Rules

* Organize handlers by event source component.
* One handler may process multiple events from the same component.
* Split a handler only when it becomes too large.
* UI updates must go through Component Controllers.
* State changes must go through Actions.
* Business operations must go through Actions.
* Event Handlers unpack Core models into primitives (or UI-local view types) before calling Component Controllers; Core models never cross into the UI layer.