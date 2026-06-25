# core/services/embedding/openai_embedding_service.py

from langchain_openai import OpenAIEmbeddings


class OpenAIEmbeddingService:
    """
    Wraps the OpenAI embeddings client.
    Core service — owns the provider specifics; nothing outside Core imports
    the embeddings library. Exposes the embeddings object for the vector store
    to consume (FAISS builds from an embeddings function).
    """

    def __init__(self, api_key: str, model: str = "text-embedding-3-small") -> None:
        self._embeddings = OpenAIEmbeddings(api_key=api_key, model=model)

    def get_embeddings(self) -> OpenAIEmbeddings:
        return self._embeddings

# core/services/embedding/openai_embedding_service.py