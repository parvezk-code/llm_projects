# core_services/chunking/code/response.py

from pydantic import BaseModel
from langchain_core.documents import Document


class CodeChunkingResponse(BaseModel):
    chunks: list[Document]
    error: str | None = None

    model_config = {"arbitrary_types_allowed": True}

    def has_chunks(self) -> bool:
        return len(self.chunks) > 0

    def has_error(self) -> bool:
        return self.error is not None