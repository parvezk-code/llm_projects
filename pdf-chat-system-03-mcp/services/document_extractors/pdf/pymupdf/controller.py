# services/document_extractors/pdf/pymupdf/controller.py

from services.document_extractors.pdf.pymupdf.service import PyMuPDFService
from services.document_extractors.pdf.pymupdf.request import PyMuPDFRequest
from services.document_extractors.pdf.pymupdf.response import PyMuPDFResponse


class PyMuPDFController:

    def __init__(self, service: PyMuPDFService):
        self._service = service

    # --- Called by MainController ---

    def extract(self, request: PyMuPDFRequest) -> PyMuPDFResponse:
        try:
            full_text, page_count = self._service.extract_text(request.file_path)
            return PyMuPDFResponse(
                full_text=full_text,
                page_count=page_count
            )
        except Exception as e:
            return PyMuPDFResponse(
                error=f"Failed to extract PDF — file may be corrupted or password-protected."
            )
