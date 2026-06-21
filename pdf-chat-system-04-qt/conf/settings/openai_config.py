# conf/settings/openai_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseSettings):
    """
    LLM-specific settings. `api_key` has no default, so the app will not start
    until it is provided (via conf/env/.env.local, .env.openAI, or the
    environment).
    """

    api_key: str
    model: str = "gpt-4.1-mini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 1000

    model_config = SettingsConfigDict(
        env_file=(
            "conf/env/.env.openAI",
            "conf/env/.env.local",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

# conf/settings/openai_config.py