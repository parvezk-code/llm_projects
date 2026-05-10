# tools/list_pdfs_in_directory/response.py

from typing import Literal
from pydantic import BaseModel


class ListPDFsResponse(BaseModel):
    success: bool


class ListPDFsSuccessResponse(ListPDFsResponse):
    success: Literal[True] = True
    directory_path: str
    pdf_files: list[str]
    total_count: int


class ListPDFsErrorResponse(ListPDFsResponse):
    success: Literal[False] = False
    error_type: str
    error_message: str