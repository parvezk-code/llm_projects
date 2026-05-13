# core_services/embedding_generators/openai/request.py

from pydantic import BaseModel
from langchain_core.documents import Document


class OpenAIEmbeddingRequest(BaseModel):
    chunks: list[Document]

    model_config = {"arbitrary_types_allowed": True}