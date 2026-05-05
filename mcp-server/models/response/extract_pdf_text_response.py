# models/response/extract_pdf_text_response.py

from typing import Literal

from pydantic import BaseModel


class ExtractPDFTextResponse(BaseModel):
    success: bool
    pdf_path: str | None = None


class ExtractPDFTextSuccessResponse(ExtractPDFTextResponse):
    success: Literal[True] = True
    pdf_path: str
    full_text: str
    page_count: int


class ExtractPDFTextErrorResponse(ExtractPDFTextResponse):
    success: Literal[False] = False
    error_type: str
    error_message: str