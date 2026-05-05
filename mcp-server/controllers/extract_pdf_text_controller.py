# controllers/extract_pdf_text_controller.py

from pathlib import Path

from models.request.extract_pdf_text_request import ExtractPDFTextRequest
from models.response.extract_pdf_text_response import (
    ExtractPDFTextResponse,
    ExtractPDFTextSuccessResponse,
    ExtractPDFTextErrorResponse,
)
from services.pdf_reader import PDFReader
from services.pdf_validator import PDFValidator


class ExtractPDFTextController:
    def __init__(self):
        self._validator = PDFValidator()
        self._reader = PDFReader()

    def execute(self, request: ExtractPDFTextRequest) -> ExtractPDFTextResponse:
        error_message = self._validator.validate(request.pdf_path)

        if error_message:
            return ExtractPDFTextErrorResponse(
                pdf_path=request.pdf_path,
                error_type="ValidationError",
                error_message=error_message,
            )

        path = Path(request.pdf_path).expanduser().resolve()
        full_text, page_count = self._reader.read(path)

        return ExtractPDFTextSuccessResponse(
            pdf_path=str(path),
            full_text=full_text,
            page_count=page_count,
        )