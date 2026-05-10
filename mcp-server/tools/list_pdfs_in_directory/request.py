# tools/list_pdfs_in_directory/request.py

from pydantic import BaseModel, Field


class ListPDFsRequest(BaseModel):
    directory_path: str = Field(
        min_length=1,
        description="Absolute path to the directory to scan for PDF files",
    )
