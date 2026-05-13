# core_services/vector_stores/faiss/request.py

from pydantic import BaseModel
from langchain_core.documents import Document


class FAISSVectorStoreRequest(BaseModel):
    chunks: list[Document]

    model_config = {"arbitrary_types_allowed": True}