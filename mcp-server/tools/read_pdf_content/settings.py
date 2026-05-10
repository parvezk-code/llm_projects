# tools/read_pdf_content/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class ReadPDFContentSettings(BaseSettings):
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: list[str] = [".pdf"]
    max_file_size_bytes: int = 50 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_file="tools/read_pdf_content/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


read_pdf_content_settings = ReadPDFContentSettings()