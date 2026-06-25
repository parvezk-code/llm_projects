# core/services/vector_store/faiss_vector_store_service.py

from langchain_community.vectorstores import FAISS

from core.models.chunk import Chunk
from core.services.embedding.openai_embedding_service import OpenAIEmbeddingService


class FaissVectorStoreService:
    """
    Builds a FAISS vector store from chunks and queries it.
    Core service — owns the FAISS specifics; the resulting store is wrapped in a
    ProjectIndex (by the Action/Gateway) and treated as opaque above Core.

    build(chunks) -> opaque FAISS store
    search(store, query, top_k) -> list[Chunk]
    """

    def __init__(self, embedding_service: OpenAIEmbeddingService) -> None:
        self._embeddings = embedding_service.get_embeddings()

    def build(self, chunks: list[Chunk]) -> FAISS:
        texts = [c.content for c in chunks]
        metadatas = [{"source_path": c.source_path} for c in chunks]
        return FAISS.from_texts(texts=texts, embedding=self._embeddings, metadatas=metadatas)

    def search(self, store: FAISS, query: str, top_k: int = 4) -> list[Chunk]:
        results = store.similarity_search(query, k=top_k)
        return [
            Chunk.create(
                source_path=doc.metadata.get("source_path", "unknown"),
                content=doc.page_content,
            )
            for doc in results
        ]

# core/services/vector_store/faiss_vector_store_service.py