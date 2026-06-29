# Doc 05 — Event Handlers (Generic)

## Purpose

- Respond to UI events and coordinate the flow between the UI and the Action layer.
- Translate domain models returned by Actions into primitives before updating the UI.

---

## Directory Structure

```text
desktop/event_handlers/
└── <component>_event_handler.py    # one handler per emitting component
```

Organise handlers by the component that emits the event. A display-only component (no signals) needs no handler.

---

## Responsibilities

- Receive the Action bundle and the component controllers they need (injected, never imported), plus any UI service (e.g. Style Manager).
- For each event: read inputs from controllers, call an Action, receive the result, unpack domain models to primitives, and update the UI through controllers.
- Catch Action failures and route them to the appropriate error surface.
- Decide threading concerns (e.g. run a slow Action on a worker thread) — Actions stay synchronous.

## Typical Flow

```text
Component signal → Event Handler method → Action → (domain result)
→ unpack to primitives → Component Controller → UI
```

---

## Rules

- Organise by emitting component; one handler may process several of that component's events.
- May access: component controllers (injected) and the Action bundle.
- Must not: import the UI layer, access Core, or access/modify State directly.
- All UI updates go through controllers; all state/business changes go through Actions.
- Unpack domain models into primitives before calling controllers (the UI never sees domain models).
- The Main Controller, not the handler, connects signals to handler methods.
