# conf/settings/retriever_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class RetrieverConfig(BaseSettings):
    """
    Settings for the RAG pipeline (extraction, chunking, embedding, retrieval).
    Non-secret; loaded from .env.retriever, overridable via .env.local.
    """
    embedding_model: str = "text-embedding-3-small"
    allowed_extensions: list[str] = [".py", ".txt", ".js", ".java"]
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 4

    model_config = SettingsConfigDict(
        env_file=("conf/env/.env.retriever", "conf/env/.env.local"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

# conf/settings/retriever_config.py