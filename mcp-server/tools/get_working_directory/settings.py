# tools/get_working_directory/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkingDirectorySettings(BaseSettings):
    WORKING_DIRECTORY: str = "~/pdfs"

    model_config = SettingsConfigDict(
        env_file="tools/get_working_directory/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


working_directory_settings = WorkingDirectorySettings()
