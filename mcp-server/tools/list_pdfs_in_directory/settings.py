# tools/list_pdfs_in_directory/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class ListPDFsSettings(BaseSettings):
    ALLOWED_EXTENSIONS: list[str] = [".pdf"]

    model_config = SettingsConfigDict(
        env_file="tools/list_pdfs_in_directory/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


list_pdfs_settings = ListPDFsSettings()