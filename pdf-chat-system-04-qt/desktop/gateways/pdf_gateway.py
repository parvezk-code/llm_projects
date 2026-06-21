# desktop/gateways/pdf_gateway.py

import os

from core.services.pdf_service import PDFService
from core.models.pdf_document import PDFDocument


class PDFGateway:
    """
    Stable interface for the PDF operations Actions need.

    In local mode it wraps the Core PDFService directly. In remote mode an
    equivalent gateway would call the API client instead — Actions see the
    same interface either way, and always receive a PDFDocument.
    """

    def __init__(self, pdf_service: PDFService):
        self._pdf_service = pdf_service

    def load_document(self, file_path: str) -> PDFDocument:
        text, page_count = self._pdf_service.extract_text(file_path)
        filename = os.path.basename(file_path)
        return PDFDocument(
            filename=filename,
            file_path=file_path,
            text=text,
            page_count=page_count,
        )

# desktop/gateways/pdf_gateway.py