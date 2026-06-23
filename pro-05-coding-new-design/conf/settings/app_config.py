# conf/settings/app_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH       = Path(__file__).resolve().parent.parent / "env" / ".env.app"
ENV_LOCAL_PATH = Path(__file__).resolve().parent.parent / "env" / ".env.local"


class AppConfig(BaseSettings):
    app_name: str
    system_prompt: str

    model_config = SettingsConfigDict(
        env_file=(str(ENV_PATH), str(ENV_LOCAL_PATH)),
        env_file_encoding="utf-8",
        extra="ignore",
    )