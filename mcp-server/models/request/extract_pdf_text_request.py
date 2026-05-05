# models/request/extract_pdf_text_request.py

from pydantic import BaseModel, Field


class ExtractPDFTextRequest(BaseModel):
    pdf_path: str = Field(
        min_length=1,
        description="Absolute path to the PDF file",
    )