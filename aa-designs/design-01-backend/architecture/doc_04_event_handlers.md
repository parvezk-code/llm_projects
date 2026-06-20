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
