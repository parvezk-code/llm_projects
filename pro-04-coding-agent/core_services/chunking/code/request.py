# core_services/chunking/code/request.py

from pydantic import BaseModel
from langchain_core.documents import Document


class CodeChunkingRequest(BaseModel):
    documents: list[Document]

    model_config = {"arbitrary_types_allowed": True}