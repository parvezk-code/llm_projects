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
* Receive ready-made Gateways from the launcher (`desktop_local/` or `desktop_remote/`).
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

## Launcher Boundary

The Main Controller is mode-agnostic. It never decides whether the app
runs in local or remote mode, and it never builds Gateway implementations
itself.

```text
desktop_local/   → builds LOCAL Gateways  → starts Main Controller
desktop_remote/  → builds REMOTE Gateways → starts Main Controller
```

* `desktop_local/` is the **local launcher**: it constructs Gateway
  implementations that call Core directly, then creates and runs Main
  Controller, passing those Gateways in.
* `desktop_remote/` is the **remote launcher**: it constructs Gateway
  implementations that call Core through `api_client/`, then creates and
  runs Main Controller, passing those Gateways in.
* The actual application entry point (e.g. `python main.py`) lives inside
  the launcher folder, not inside `desktop/`.
* Main Controller only ever receives Gateways — it has no knowledge of
  which mode produced them.

---

## Must Not

* Contain business logic.
* Perform application workflows.
* Access Core directly.
* Update State directly.
* Manipulate UI widgets directly.
* Contain event-handling logic.
* Decide local vs remote mode.
* Build Gateway implementations itself.

---

## Design Rules

* Only one Main Controller per application.
* Acts as the application's composition root.
* Responsible for object creation and wiring.
* Keeps other modules unaware of construction details.