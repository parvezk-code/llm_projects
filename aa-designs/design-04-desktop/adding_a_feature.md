# Adding a Feature — End-to-End Recipe

How to add a new use case (a workflow, a mode, a button, a panel) across all layers
without breaking the architecture. Build **bottom-up** so each layer's dependency
already exists when you need it, then **wire top-down**.

Each step links to the layer's own rule doc — follow those for the detail; this doc
is the order and the checklist.

---

## The Order

```text
1. Config          → settings class + .env + bundle                  (config_rules.md)
2. Core            → model(s) + service(s) + workflow (if needed)    (core_rules.md)
3. Gateway         → method or new gateway + bundle                  (gateway_rules.md)
4. State           → field(s) + event-shaped method                  (state_and_controller_rules.md)
5. Action          → one execute() + bundle field                    (action_rules.md)
6. UI Component    → dumb renderer + signal                          (ui_component_and_controller_rules.md, Part A)
7. UI Controller   → bind_* + event-shaped method                    (ui_component_and_controller_rules.md, Part B)
8. Event Handler   → on_<event> orchestration                        (event_handler_rules.md)
9. Main Controller → create + wire + (unlock)                        (main_controller_rules.md, Part B)
10. Launcher       → load config → build Core → build gateway        (main_controller_rules.md, Part A)
```

Config comes first because the Core services are built from config.
If the feature requires a larger domain process, build a Core workflow from those
services before constructing the gateway. Lower layers (1–5) are pure logic with no UI
dependency and can be developed and tested before wiring them into the application.

---

## Per-Step Checklist

### 1. Config — settings class + .env + bundle
*(config_rules.md)*

- Add a `*_config.py` settings class (one per area) only if the feature needs new
  settings. Required secrets have **no default**; everything else gets a sensible one.
- Use `SettingsConfigDict` with `env_file=("conf/env/.env.<area>", "conf/env/.env.local")`
  (`.env.local` last so it wins), `extra="ignore"`.
- Add the committed `.env.<area>` (non-secret defaults) and, if needed, an
  `.env.<area>.example` template. Secrets go only in the gitignored `.env.local`.
- Add the new settings class to `ConfigBundle` so `load_config()` builds it.
- Skip this step if the feature needs no new settings.

### 2. Core — model(s) + service(s) + workflow (if needed)

*(core_rules.md)*

* Add a **frozen** `@dataclass` model if there is new domain data. Give it factory
  constructors; no `to_dict()`, no business logic.
* Add one or more **services** under `core/services/<area>/`. Each service performs
  one reusable capability.
* If the feature requires coordinating several services in a fixed sequence, add a
  **workflow** under `core/workflows/<area>/`. The workflow owns the domain
  algorithm and composes the required services.
* Services should remain independent. A service should not coordinate several
  other services.
* Skip the workflow if the feature is already handled by a single service.


### 3. Gateway — method or new gateway
*(gateway_rules.md)*

- **Same external concern** as an existing gateway → add a method (`get_rag_reply`).
- **New external concern** → add a new gateway **and** a field on `GatewayBundle`.
- Keep it thin: receive pre-shaped data from the action, delegate to Core, return a
  domain model. No shaping, no logic.

### 4. State — field(s) + event-shaped method
*(state_and_controller_rules.md)*

- Add field(s) to `AppState` (data only, primitive or passive frozen model).
- Add accessor methods to `StateController`.
- If the feature's event writes **several fields together**, add **one event-shaped
  method** (`reset_on_<event>()`) instead of fine-grained setters.
- Skip if the feature has no persistent state.

### 5. Action — one workflow + bundle field
*(action_rules.md)*

- One application task, one `execute(...)`, constructed `(state_controller, gateways)`.
- Shape transport here; set `is_processing`; commit atomically **on success**;
  return domain model(s).
- Add a field to `ActionBundle`.
- A mode variant is a **separate action** — never `if mode ==` inside one.

### 6. UI Component — dumb renderer + signal
*(ui_component_and_controller_rules.md, Part A)*

- Build with `_create_widgets / _create_layout / _connect_child_signals`.
- Leaf widgets set `objectName` for QSS; no inline styles.
- Emit **one signal per distinct intent**; expose primitive accessors only.
- Reuse existing components where possible (many were built early and sit disabled).

### 7. UI Component Controller — bind_* + event-shaped method
*(ui_component_and_controller_rules.md, Part B)*

- One `bind_<signal>(method)` per component signal.
- For a multi-op event, add **one event-shaped method** (`reset_on_<event>()`) doing
  all of that component's work for the event.
- Primitives only; no business logic; never talk to another controller.

### 8. Event Handler — on_<event> orchestration
*(event_handler_rules.md)*

- New file under `event_handlers/<component>/`, class `…Handler`, method `on_<event>`.
- Read input → **guard** (if any) → call **one** action → call **one** event-shaped
  method per affected controller.
- Unpack domain models to primitives before touching controllers.
- Route errors to the correct surface (chat bubble vs status banner).
- Run on a `Worker` thread if the action is slow; hold the worker reference.

### 9. Main Controller — create + wire + (unlock)
*(main_controller_rules.md, Part B)*

- `_create_actions`: add the new action to the bundle.
- `_create_event_handlers`: create the handler, stored as `self._<name>_handler`
  (prevents GC from killing the signal connection).
- `_wire_events`: bind the component signal to the handler method.
- Bump `UNLOCK_LEVEL` only if the feature unlocks UI controls.

### 10. Launcher — load config + build Core + gateway

*(main_controller_rules.md, Part A)*

* `load_config()` already returns the new settings (from step 1) on the bundle.
* Build the required **Core services** from configuration.
* If the feature includes a Core workflow, build it by supplying the required
  Core services.
* Build or extend the gateway and and add it to `GatewayBundle`. Inject either the Core service or the Core
  workflow, depending on what the gateway exposes.
* This is the **only** place where configuration is read and where Core objects
  and Gateways are constructed.


---

## The Cross-Cutting Rule — One Method Per Event

For any event that touches multiple things, the **one-method-per-event** principle
applies in three places at once, all sharing the same intent-named verb:

```text
Handler.on_<event>()
  → Action.execute()            → StateController.reset_on_<event>()   (one state method)
  → ChatAreaController.reset_on_<event>()                              (one per controller)
  → StatusBarController.reset_on_<event>()
  → InputBarController.reset_on_<event>()
  → ToolbarController.reset_on_<event>()
```

- The **handler** is the only orchestrator — it knows *which* layers an event touches.
- Each **controller / state method** knows *what* its own layer does for that event.
- The shared verb (`reset_on_clear_chat`) makes the whole event traceable end-to-end
  by a single name.

Busy toggling (`set_enabled` during a threaded run) is the allowed fine-grained
exception — it is a UI-state gate, not an event reset.

---

## What To Skip When

| Feature shape | Steps you can skip |
|---|---|
| No new settings | 1 |
| Reuses existing model/service | 2 |
| Reuses existing external concern | new gateway (still add a method) |
| No persistent state | 4 |
| Reuses an existing component (e.g. unlocking a disabled one) | 6 |
| Pure logic change, no UI | 6, 7, 8, and wiring in 9 |

---

## Worked Example — the RAG "Load Project" feature (Level 2)

```text
1. Config    → RetrieverConfig + .env.retriever; added to ConfigBundle
2. Core      → Document, Chunk, ProjectIndex models;
               extractor, chunker, embedding, vector_store services, index_builder_workflow
3. Gateway   → new IndexGateway, delegates to IndexBuilderWorkflow + bundle field
4. State     → project_path, project_index fields; set/get/clear accessors
5. Action    → LoadProjectAction.execute(path); send_rag action; bundle fields
6. Component → reused (folder_picker, load_project_button already existed)
7. Controller→ folder_picker bind_folder_selected; toolbar set_project_name
8. Handler   → folder_picker/folder_selected_handler.py (threaded build)
               + send router on_send_rag with no-project guard
9. Main Ctrl → create handlers, wire signals, UNLOCK_LEVEL = 2
10. Launcher → load RetrieverConfig; build the four RAG services, IndexBuilderWorkflow + IndexGateway
```

# Adding a Feature — End-to-End Recipe