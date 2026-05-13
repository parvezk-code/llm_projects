# services/retriever/pipeline/response.py

from pydantic import BaseModel
from langchain_core.vectorstores import VectorStoreRetriever


class RetrieverPipelineResponse(BaseModel):
    retriever: VectorStoreRetriever | None = None
    error: str | None = None

    model_config = {"arbitrary_types_allowed": True}

    def has_retriever(self) -> bool:
        return self.retriever is not None

    def has_error(self) -> bool:
        return self.error is not None