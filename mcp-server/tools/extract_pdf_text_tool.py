# tools/extract_pdf_text_tool.py

from pydantic import ValidationError

from controllers.extract_pdf_text_controller import ExtractPDFTextController
from models.request.extract_pdf_text_request import ExtractPDFTextRequest
from models.response.extract_pdf_text_response import (
    ExtractPDFTextResponse,
    ExtractPDFTextErrorResponse,
)


controller = ExtractPDFTextController()


def extract_pdf_text(pdf_path: str) -> ExtractPDFTextResponse:
    """Extract all text from a PDF file and return it with metadata."""

    try:
        request = ExtractPDFTextRequest(pdf_path=pdf_path)

    except ValidationError as error:
        return ExtractPDFTextErrorResponse(
            pdf_path=pdf_path,
            error_type="ValidationError",
            error_message=str(error),
        )

    return controller.execute(request)