# Doc 01 — Architecture Overview (Generic)

A layered desktop-application architecture:
`UI → Event Handlers → Actions → State Controller + Gateways → Core`,
with a launcher that decides local-vs-remote and a composition root that wires everything.

This document set is app-agnostic. Replace the placeholder names
(`<feature>`, `<topic>`, `<workflow>`, `<X>Service`, `DomainModel`) with your own.

---

## Goals

- Separate UI from business logic.
- Keep layers loosely coupled and independently testable.
- Allow the same app to run locally or remotely by changing only the launcher.
- Make dependencies flow in one direction so changes stay contained.

---

## Generic Directory Structure

```text
app_root/
├── conf/                  # typed configuration + env files
├── core/                  # business logic: services + domain models
│   ├── services/
│   └── models/
├── desktop/               # runtime (mode-agnostic)
│   ├── state/
│   ├── state_controller/
│   ├── gateways/
│   ├── actions/
│   ├── action_bundles/
│   ├── event_handlers/
│   └── main_controller.py
├── desktop_local/         # LOCAL launcher + entry point
│   └── main.py
├── desktop_remote/        # REMOTE launcher (optional)
└── ui/                    # presentation
    ├── components/
    ├── controllers/
    ├── pages/
    ├── screen_manager.py
    ├── main_window.py
    └── ui_bundle.py
```

---

## The Layers

- **conf/** — typed settings from `.env` files; consumed only by the launcher.
- **core/** — business logic. `services/` perform operations; `models/` hold domain data. Knows nothing above it.
- **desktop/** — application runtime: state, gateways, actions, event handlers, and the composition root. Mode-agnostic.
- **launcher (desktop_local / desktop_remote)** — builds the Gateways for its mode and runs the Main Controller.
- **ui/** — dumb components, their controllers, pages, and a composition root that returns a controller bundle.

---

## Dependency Direction

```text
UI
 ↓
Event Handlers
 ↓
Actions
 ↓
State Controller  +  Gateways
                        ↓
                      Core
```

Lower layers never import higher layers. `conf/` is read by the launcher only.

---

## Request / Response Flow

```text
User → UI → Event Handler → Action → Gateway → Core
Core → Gateway → Action → (State update) → Event Handler → Component Controller → UI → User
```

---

## Recipe — Adding One Feature End to End

For a new user-facing capability, touch the layers top-down:

1. **UI** — add/extend a component (dumb renderer + signal) and its controller (`bind_*` + operation methods, primitives only).
2. **Event Handler** — add a handler method on the emitting component's handler: read inputs, call an Action, unpack the result to primitives, update controllers.
3. **Action** — add one `execute(...)` workflow under the right `actions/<topic>/`: read/write state via the State Controller, call a Gateway, return a result.
4. **Gateway** — if the work touches an external system, add a method to the relevant gateway (returns a domain model).
5. **State** — add a field to the state object and accessor methods to the State Controller, if the feature has persistent data.
6. **Core** — add a service operation and/or domain model for the actual business logic.
7. **Wiring** — bind the new component signal to the new handler method in the Main Controller.

---

## Rules

- Dependencies flow downward only; never import upward.
- UI consumes primitives; it never imports Core or names domain models.
- Event Handlers never import the UI layer; controllers are injected.
- Only Actions read/write State and call Gateways.
- Core is independent of UI, State, Actions, Gateways, and launchers.
- The launcher chooses the mode; nothing above the Gateways knows the mode.
