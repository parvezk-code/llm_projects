# conf/settings/retriever_config.py

from pydantic_settings import BaseSettings
from pathlib import Path


class RetrieverConfig(BaseSettings):
    chunk_size: int
    chunk_overlap: int
    allowed_extensions: list[str]
    embedding_model: str

    model_config = {
        "env_file": Path(__file__).parent.parent / "env" / ".env.retriever",
        "env_file_encoding": "utf-8",
    }