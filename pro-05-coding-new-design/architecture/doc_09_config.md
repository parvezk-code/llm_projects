# Configuration — Design Rules

App-specific rules for typed, validated settings loaded from `.env` files, consumed
only by the launcher, kept mode-neutral so any launcher can build Core services.

---

## Part A — Settings Class Rules

1. **One settings class per area.** Each concern has its own class
   (`AppConfig`, `OpenAIConfig`, `RetrieverConfig`), built on
   `pydantic-settings.BaseSettings` so values are typed, validated, and coerced.

2. **Required values have no default.** Secrets/credentials that must be present
   (`api_key`) have no default, so startup fails fast with a clear error if missing.
   Everything else has a sensible default.

3. **Always use `SettingsConfigDict`, never a plain dict.** `model_config` is a
   `SettingsConfigDict` with `env_file`, `env_file_encoding="utf-8"`, and
   `extra="ignore"` (so unrelated env vars never break loading).

4. **`.env.local` is always the last file in the tuple.** Each class loads from
   `(".env.<area>", ".env.local")`; the later file wins, so secrets and local
   overrides in `.env.local` take precedence over committed defaults.

5. **Field names are the contract.** Field names map to env keys and to the
   primitives passed to Core services. Where a service parameter differs from a
   config field (`llm_temperature → temperature`), the mapping happens in the
   launcher, not in the config class.

---

## Part B — Bundle & Loading Rules

1. **One frozen `ConfigBundle` aggregates all settings.** A
   `@dataclass(frozen=True)` holds `app`, `openai`, `retriever`. A single
   `load_config()` instantiates and validates all of them and returns the bundle.

2. **`load_config()` is called once, by the launcher only.** Configuration is never
   imported by UI, handlers, actions, state, gateways, or Core. Only the launcher
   reads it and uses it to build services and gateways.

3. **Fail fast with a friendly message.** If a required value is missing,
   `load_config()` raises; the launcher catches it, prints a clear message pointing
   at `conf/env/.env.local`, and exits before building anything.

---

## Part C — File Split Rules

1. **Secret vs non-secret split across files.**

   ```
   .env.app             non-secret app settings        (committed)
   .env.openAI          non-secret LLM settings        (committed)
   .env.retriever       non-secret RAG settings        (committed)
   .env.<area>.example  template documenting keys      (committed)
   .env.local           secrets + local overrides      (gitignored, user-created)
   ```

2. **Secrets never committed.** The `api_key` lives only in `.env.local`, which is
   gitignored and created by the user. Committed files hold non-secret defaults and
   `.example` templates only.

3. **Paths are relative to the project root.** `env_file` paths resolve from the
   working directory, so the app must be launched from the project root
   (`python -m desktop_local.main`).

4. **`conf/` lives at the project root.** Config is shared, unchanged, by every
   launcher (local now, remote later), so it sits at the root rather than inside any
   one launcher.

---

## Why this split

- Typed settings catch misconfiguration at startup, not mid-run.
- The secret/non-secret file split keeps credentials out of version control while
  documenting every required key.
- Because only the launcher reads config and maps it onto Core services, config stays
  a single, mode-neutral entry point — nothing else in the app knows env files exist.

# Configuration — Design Rules