# conf/settings.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVER_NAME: str = "pdf-reader-server"
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: list[str] = [".pdf"]

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    class Config:
        env_file = "conf/.env"
        env_file_encoding = "utf-8"


settings = Settings()