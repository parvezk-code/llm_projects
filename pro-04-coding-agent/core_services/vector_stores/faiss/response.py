# core_services/vector_stores/faiss/response.py

from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever


class FAISSVectorStoreResponse(BaseModel):
    retriever: VectorStoreRetriever | None = None
    error: str | None = None

    model_config = {"arbitrary_types_allowed": True}

    def has_retriever(self) -> bool:
        return self.retriever is not None

    def has_error(self) -> bool:
        return self.error is not None