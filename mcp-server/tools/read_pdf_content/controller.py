# tools/read_pdf_content/controller.py

from pathlib import Path

from tools.read_pdf_content.request import ReadPDFContentRequest
from tools.read_pdf_content.response import (
    ReadPDFContentResponse,
    ReadPDFContentSuccessResponse,
    ReadPDFContentErrorResponse,
)
from tools.read_pdf_content.pdf_validator import PDFValidator
from tools.read_pdf_content.pdf_reader import PDFReader


validator = PDFValidator()
reader = PDFReader()


class ReadPDFContentController:

    def execute(self, request: ReadPDFContentRequest) -> ReadPDFContentResponse:
        try:
            error = validator.validate(request.pdf_path)

            if error:
                return ReadPDFContentErrorResponse(
                    error_type="ValidationError",
                    error_message=error,
                )

            path = Path(request.pdf_path).expanduser().resolve()
            full_text, page_count = reader.read(path)

            return ReadPDFContentSuccessResponse(
                pdf_path=str(path),
                full_text=full_text,
                page_count=page_count,
            )

        except Exception as error:
            return ReadPDFContentErrorResponse(
                error_type="UnexpectedError",
                error_message=str(error),
            )
