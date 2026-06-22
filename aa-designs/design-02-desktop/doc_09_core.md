# Doc 09 — Core (Generic)

## Purpose

- Hold business logic and domain data.
- Stay independent of UI, application flow, state management, and infrastructure.
- Be reusable unchanged in local or remote mode.

---

## Directory Structure

```text
core/
├── services/      # business operations
├── models/        # domain data
├── processors/    # processing logic (optional)
├── validators/    # validation rules (optional)
└── utils/         # core-only helpers (optional)
```

The internal structure may vary per app; `services/` and `models/` are the common minimum.

---

## Responsibilities

- **Services** — perform single, well-scoped business operations; wrap third-party libraries/SDKs here so provider specifics stay inside Core.
- **Models** — passive domain data (prefer immutable). Provide factory constructors for convenience, but no workflow logic and no transport/serialisation shaping (that belongs in Actions).
- Apply domain rules, process data, validate constraints, and return results or models.

## Typical Flow

```text
Action → Gateway → Core
```

---

## Rules

- Core must not access UI, State, Actions, Gateways, or launcher code.
- Models store/represent data only; keep them immutable where practical.
- Services own external-library specifics; nothing outside Core imports those libraries.
- Workflow orchestration does not belong in Core; business rules do.
- Core must be usable identically in local and remote modes.
