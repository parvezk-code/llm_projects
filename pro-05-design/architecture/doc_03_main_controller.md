# Main Controller

## Purpose

The Main Controller is the single orchestrator of the application.

It wires together UI, Event Handlers, Actions, State, and Gateways.

---

## Directory Structure

```text
desktop/
└── main_controller.py     # Application orchestrator
```

---

## Responsibilities

* Create application dependencies.
* Create state objects.
* Create State Controller.
* Create Gateways.
* Create Actions.
* Create Action Bundles.
* Create Event Handler Bundles.
* Create pages.
* Receive controller bundle from pages.
* Wire component events to event handlers.
* Define application startup sequence.

---

## Event Wiring

Example:

```text
Component Event
        ↓
Event Handler Method
```

The Main Controller performs all event wiring.

---

## Dependency Wiring

Example:

```text
State
    ↓
State Controller
    ↓
Actions
    ↓
Action Bundles
    ↓
Event Handlers
```

The Main Controller creates and connects all dependencies.

---

## Must Not

* Contain business logic.
* Perform application workflows.
* Access Core directly.
* Update State directly.
* Manipulate UI widgets directly.
* Contain event-handling logic.

---

## Design Rules

* Only one Main Controller per application.
* Acts as the application's composition root.
* Responsible for object creation and wiring.
* Keeps other modules unaware of construction details.
