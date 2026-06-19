# Desktop Layer

## Purpose

The Desktop layer contains the application runtime structure for running the UI application.

It is responsible for wiring together all layers into a working application instance.

It does not contain UI, business logic, or domain rules.

---

## Directory Structure

```

desktop/
|
├── main_controller.py              # Application composition root
│
├── state/                          # Application state objects
│
├── state_controller/               # Single access layer for state
│   └── state_controller.py
│
├── gateways/                       # External access abstraction
│
├── actions/                        # Application workflows
│
├── action_bundles/                 # Grouped action interfaces
│
└── event_handlers/                 # UI event processing layer


```

---

## Responsibilities

### Application Composition

* Create all application objects.
* Initialize state, gateways, and actions.
* Build dependency graph.
* Inject dependencies into handlers.

---

### Wiring

* Connect UI events to event handlers.
* Provide action bundles to event handlers.
* Provide gateway bundle to actions.
* Provide state controller to actions.

---

### Runtime Control

* Define application startup sequence.
* Initialize local or remote mode setup.
* Manage application bootstrapping only.

---

## Main Controller Responsibilities

* Acts as the single entry point of the application.
* Wires all modules together.
* Ensures correct dependency injection.
* Does not execute business logic.
* Does not handle UI logic.
* Does not manage state directly.

---

## Design Rules

* Only one Main Controller exists per application.
* Desktop layer is purely orchestration.
* No business logic is allowed in this layer.
* No UI rendering is allowed in this layer.
* No domain logic is allowed in this layer.
* All dependencies are explicitly wired here.
