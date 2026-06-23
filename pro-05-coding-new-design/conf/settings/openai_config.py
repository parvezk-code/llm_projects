# conf/settings/openai_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseSettings):
    api_key: str                        # required — no default; app fails fast if missing
    model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 1000

    model_config = SettingsConfigDict(
        env_file=("conf/env/.env.openAI", "conf/env/.env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

# conf/settings/openai_config.py