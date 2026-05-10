# tools/read_pdf_content/request.py

from pydantic import BaseModel, Field


class ReadPDFContentRequest(BaseModel):
    pdf_path: str = Field(
        min_length=1,
        description="Absolute path to the PDF file",
    )
