# tools/read_pdf_content/tool.py

from pydantic import ValidationError

from tools.read_pdf_content.request import ReadPDFContentRequest
from tools.read_pdf_content.response import (
    ReadPDFContentResponse,
    ReadPDFContentErrorResponse,
)
from tools.read_pdf_content.controller import ReadPDFContentController


controller = ReadPDFContentController()


def read_pdf_content(pdf_path: str) -> ReadPDFContentResponse:
    """Read and return the full text content of a PDF file."""

    try:
        request = ReadPDFContentRequest(pdf_path=pdf_path)

    except ValidationError as error:
        return ReadPDFContentErrorResponse(
            error_type="ValidationError",
            error_message=str(error),
        )

    return controller.execute(request)
