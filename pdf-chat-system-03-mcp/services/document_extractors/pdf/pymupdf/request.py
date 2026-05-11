# services/document_extractors/pdf/pymupdf/request.py

from pydantic import BaseModel, field_validator


class PyMuPDFRequest(BaseModel):
    file_path: str

    @field_validator("file_path")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if len(v.strip()) < 1:
            raise ValueError("file_path must not be empty")
        return v
