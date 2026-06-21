# Doc 11 — Configuration

## Purpose

- Provide typed, validated application settings loaded from `.env` files.
- Keep secrets out of the codebase while documenting what is required.
- Stay mode-neutral: settings live at the project root so any launcher (local now, remote/API server later) can build Core services from them.

---

## Directory Structure

```text
conf/
├── __init__.py
├── settings/
│   ├── __init__.py
│   ├── app_config.py       # AppConfig    — shared/global settings
│   ├── openai_config.py    # OpenAIConfig — LLM-specific settings
│   └── config_bundle.py    # ConfigBundle + load_config()
└── env/
    ├── .env.app            # non-secret app settings (committed)
    ├── .env.openAI         # non-secret LLM settings (committed)
    └── .env.openAI.example # template documenting required keys (committed)
```

Not committed (created by the user, gitignored): `conf/env/.env.local` — holds the secret `api_key`.

---

## Implementation

- Built on **pydantic-settings** (`BaseSettings`), so values are typed, validated, and coerced.
- **`AppConfig`**
  - `app_name: str = "Chat App"`.
  - Loads from `conf/env/.env.app`.
- **`OpenAIConfig`**
  - `api_key: str` (no default — **required**), `model: str = "gpt-4.1-mini"`, `llm_temperature: float = 0.2`, `llm_max_tokens: int = 1000`.
  - Loads from the tuple `("conf/env/.env.openAI", "conf/env/.env.local")`; the later file (`.env.local`) overrides the earlier one, so secrets in `.env.local` win over committed non-secret defaults.
- **`ConfigBundle`** — frozen dataclass holding `app: AppConfig` and `openai: OpenAIConfig`.
  - **`load_config() -> ConfigBundle`** instantiates both; raises (pydantic `ValidationError`) if a required value such as `api_key` is missing.
- **Consumption** — only the launcher calls `load_config()`. It maps `OpenAIConfig` fields onto the Core service: `llm_temperature → temperature`, `llm_max_tokens → max_tokens`.

## File Split (secret vs non-secret)

```text
.env.app            app_name                                  (committed)
.env.openAI         model, llm_temperature, llm_max_tokens    (committed, non-secret)
.env.local          api_key=sk-...                            (gitignored, user-created)
.env.openAI.example template for the above                    (committed)
```

## Startup Behaviour

- `python -m desktop_local.main` calls `load_config()`.
- If `api_key` is absent everywhere, startup fails fast; the launcher prints a friendly message pointing at `conf/env/.env.local` and exits.

---

## Rules

- Configuration is consumed by the launcher only; it is never imported by UI, Event Handlers, Actions, State, Gateways, or Core.
- Secrets live in `conf/env/.env.local` (gitignored); non-secret values live in committed `.env.app` / `.env.openAI`.
- `api_key` is required — the app does not start without it.
- `env_file` paths are resolved relative to the current working directory, so the app must be launched from the project root.
- Settings module filenames are snake_case; `.env` filenames are kept as given (`.env.app`, `.env.openAI`, `.env.local`).
- `conf/` sits at the project root so it is shared, unchanged, by local and future remote launchers.
