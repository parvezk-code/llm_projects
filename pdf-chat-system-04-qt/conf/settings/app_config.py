# conf/settings/app_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """Shared / global application settings."""

    app_name: str = "Chat App"

    model_config = SettingsConfigDict(
        env_file="conf/env/.env.app",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# conf/settings/app_config.py