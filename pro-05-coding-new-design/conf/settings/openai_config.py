# conf/settings/openai_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH       = Path(__file__).resolve().parent.parent / "env" / ".env.openai"
ENV_LOCAL_PATH = Path(__file__).resolve().parent.parent / "env" / ".env.local"


class OpenAIConfig(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    temperature: float = 0.2
    max_tokens: int = 2048

    model_config = SettingsConfigDict(
        env_file=(str(ENV_PATH), str(ENV_LOCAL_PATH)),
        env_file_encoding="utf-8",
        extra="ignore",
    )