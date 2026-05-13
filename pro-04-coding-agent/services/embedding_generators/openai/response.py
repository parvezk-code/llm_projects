# core_services/embedding_generators/openai/response.py

from pydantic import BaseModel
from langchain_community.vectorstores import FAISS


class OpenAIEmbeddingResponse(BaseModel):
    embeddings: list[list[float]]
    error: str | None = None

    def has_embeddings(self) -> bool:
        return len(self.embeddings) > 0

    def has_error(self) -> bool:
        return self.error is not None