# tools/read_pdf_content/response.py

from typing import Literal
from pydantic import BaseModel


class ReadPDFContentResponse(BaseModel):
    success: bool


class ReadPDFContentSuccessResponse(ReadPDFContentResponse):
    success: Literal[True] = True
    pdf_path: str
    full_text: str
    page_count: int


class ReadPDFContentErrorResponse(ReadPDFContentResponse):
    success: Literal[False] = False
    error_type: str
    error_message: str