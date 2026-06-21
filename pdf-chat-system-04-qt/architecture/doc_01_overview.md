# Doc 01 — Architecture Overview

## Purpose

- Separate UI from business logic.
- Keep modules loosely coupled and independently testable.
- Support local execution now, and remote execution later without changing the upper layers.
- Make local-vs-remote a launcher decision, invisible to everything above the Gateways.

---

## Directory Structure

```text
chat_pdf/                  # project root (run commands from here)
├── conf/                  # typed configuration (pydantic-settings) + .env files
├── core/                  # business logic: services + domain models
├── desktop/               # application runtime (mode-agnostic)
├── desktop_local/         # LOCAL launcher + entry point (python -m desktop_local.main)
├── ui/                    # presentation layer
├── README.md
├── requirements.txt
└── .gitignore
```

Not implemented yet (left room for, per the original design): `desktop_remote/`, `api_server/`, `api_client/`.

---

## Layers (implementation)

- **conf/** — typed settings loaded from `conf/env/.env*` files via pydantic-settings. Consumed only by the launcher.
- **core/** — business logic: `services/` (LLM, PDF) and `models/` (domain data). Independent of UI, State, Gateways, and Actions.
- **desktop/** — runtime wiring and workflows: `state/`, `state_controller/`, `gateways/`, `actions/`, `action_bundles/`, `event_handlers/`, and `main_controller.py`. Mode-agnostic.
- **desktop_local/** — the local launcher: builds LOCAL Gateways (wrapping Core directly) and runs the Main Controller. Holds the entry point.
- **ui/** — presentation: `components/`, `controllers/`, `pages/`, `screen_manager.py`, `main_window.py`, `ui_bundle.py`, `style_manager.py`, `styles/`.

---

## Mode Ownership

- The **launcher** decides the mode. `desktop_local/` builds LOCAL Gateways that call Core directly.
- `desktop_remote/` / `api_server/` / `api_client/` are not built; when added they only change which Gateways the launcher constructs.
- The Main Controller and everything above the Gateways is mode-agnostic and unchanged between modes.

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

- `conf/` is read by the launcher only.
- Dependencies flow downward; lower layers never import higher layers.

---

## High-Level Flow

```text
User → UI → Event Handler → Action → Gateway → Core
Core → Gateway → Action → (State update) → Event Handler → Component Controller → UI → User
```

---

## Rules

- Dependencies flow downward only; a lower layer never imports a higher layer.
- UI never imports Core logic or Core models; it consumes primitives only.
- Event Handlers never import the UI layer; controllers are injected into them.
- Only Actions read/write State (through the State Controller) and call Gateways.
- Core is independent of UI, State, Actions, Gateways, and the launcher.
- The mode (local/remote) is chosen by the launcher, never by Main Controller or anything below it.
- The app is launched from the project root as a module (`python -m desktop_local.main`).
