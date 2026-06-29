# Doc 10 — Configuration (Generic)

## Purpose

- Provide typed, validated settings loaded from environment/`.env` files.
- Keep secrets out of the codebase while documenting required values.
- Stay mode-neutral so any launcher can build Core services from it.

---

## Directory Structure

```text
conf/
├── settings/
│   ├── <area>_config.py    # one settings group per area (app, external service, ...)
│   └── config_bundle.py    # aggregates settings + a loader
└── env/
    ├── .env.<area>         # non-secret settings (committed)
    ├── .env.<area>.example # template documenting required keys (committed)
    └── .env.local          # secrets / local overrides (gitignored, user-created)
```

---

## Responsibilities

- Define one typed settings class per area (validated, type-coerced).
- Required values (e.g. credentials) have **no default**, so startup fails fast if missing.
- Split secret vs non-secret across files; a local override file takes priority over committed defaults.
- A bundle aggregates the settings groups; a `load_config()` builds and validates them.
- Only the launcher loads config and uses it to build Gateways/Core services.

## Startup Behaviour

- The launcher loads config first; if a required value is missing it fails fast with a clear message and exits.

---

## Rules

- Config is consumed by the launcher only; never imported by UI, Event Handlers, Actions, State, Gateways, or Core.
- Secrets live in the gitignored local file; non-secret values live in committed files.
- Required credentials have no default — the app does not start without them.
- If env-file paths are relative, the app must be launched from the project root.
- Config lives at the project root so it is shared, unchanged, by every launcher.
