# core_services/document_extractors/text/plain/response.py

from pydantic import BaseModel
from langchain_core.documents import Document


class PlainTextExtractorResponse(BaseModel):
    documents: list[Document]
    error: str | None = None

    model_config = {"arbitrary_types_allowed": True}

    def has_documents(self) -> bool:
        return len(self.documents) > 0

    def has_error(self) -> bool:
        return self.error is not None