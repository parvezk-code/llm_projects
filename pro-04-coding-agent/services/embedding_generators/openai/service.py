# core_services/embedding_generators/openai/service.py

import logging
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class OpenAIEmbeddingService:

    def __init__(self, model: str, api_key: str) -> None:
        self._embeddings = OpenAIEmbeddings(
            model=model,
            api_key=api_key,
        )

    def embed(self, chunks: list[Document]) -> list[list[float]]:
        texts = [chunk.page_content for chunk in chunks]
        vectors = self._embeddings.embed_documents(texts)
        logger.info(f"Generated embeddings for {len(texts)} chunks")
        return vectors

    def get_embeddings_model(self) -> OpenAIEmbeddings:
        return self._embeddings