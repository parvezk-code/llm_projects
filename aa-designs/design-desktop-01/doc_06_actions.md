# Doc 06 — Actions (Generic)

## Purpose

- Implement application workflows.
- Coordinate state changes (via the State Controller) and external work (via Gateways).
- Return results to Event Handlers; perform no UI work.

---

## Directory Structure

```text
desktop/
├── actions/
│   └── <topic>/
│       └── <workflow>_action.py     # one workflow per file
└── action_bundles/
    └── action_bundle.py             # bundle(s) of actions for the handlers
```

Organise actions by business/domain topic. Use one bundle, or a few topic bundles, to hand actions to Event Handlers.

---

## Responsibilities

- Construct each action with `(state_controller, gateways)`; expose a single `execute(...)`.
- One action represents one workflow:
  - read state (via the State Controller),
  - call a Gateway (which reaches Core),
  - write state (via the State Controller),
  - return a result (often a domain model) to the Event Handler.
- Keep writes atomic where it matters: commit state changes only after the external call succeeds, so a failure leaves state consistent.
- Do any model-to-transport shaping (e.g. domain model → request payload) here, not in the model or the gateway.

## Typical Flow

```text
Event Handler → Action → (read State) → Gateway → Core → (write State) → return
```

---

## Rules

- One action = one workflow; organise by domain topic.
- Actions are the only layer that reads/writes State and calls Gateways.
- May access: the State Controller and the Gateway bundle. Nothing else.
- Must not: access UI, controllers, Event Handlers, or perform widget work.
- Actions are synchronous and UI-agnostic; threading is an Event Handler concern.
- Raise failures (after leaving state consistent); let Event Handlers handle errors.
