# Doc 08 — Gateways (Generic)

## Purpose

- Provide a stable interface between Actions and external systems.
- Hide whether functionality is local (Core in-process) or remote (via an API client).
- Return domain-shaped results so Actions are mode-independent.

---

## Directory Structure

```text
desktop/gateways/
├── gateway_bundle.py       # bundle of all gateways
└── <topic>_gateway.py      # one gateway per external concern
```

Create a gateway only where there is a backing capability (a Core service now, an API client later). Do not create empty gateways.

---

## Responsibilities

- Expose only the operations Actions need; hide implementation and mode.
- Delegate to a Core service (local) or an API client (remote) and adapt the result into a domain model.
- The Gateway bundle is a single object holding all gateways, built by the launcher and passed down.

## Local vs Remote

```text
LOCAL  : Action → Gateway → Core
REMOTE : Action → Gateway → API Client → API Server → Core
```

Same interface in both; only the gateway's internals differ.

---

## Rules

- One gateway per external concern.
- May access: Core (local) or the API client (remote).
- Must not: access UI, controllers, Event Handlers, or State.
- Contain no business logic; delegate and adapt only.
- Local and remote gateways expose the same interface so Actions never change between modes.
