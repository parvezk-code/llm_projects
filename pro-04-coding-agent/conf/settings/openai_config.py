from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / "env" / ".env.openai"


class OpenAIConfig(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o"
    temperature: float = 0.2
    max_tokens: int = 2048

    model_config = {"env_file": str(ENV_PATH), "env_file_encoding": "utf-8"}
