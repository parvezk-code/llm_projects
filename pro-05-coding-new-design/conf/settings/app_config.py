# conf/settings/app_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    app_name: str = "Coding Agent"

    model_config = SettingsConfigDict(
        env_file="conf/env/.env.app",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# conf/settings/app_config.py