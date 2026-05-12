from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / "env" / ".env.app"


class AppConfig(BaseSettings):
    app_name: str
    system_prompt: str

    model_config = {"env_file": str(ENV_PATH), "env_file_encoding": "utf-8"}
