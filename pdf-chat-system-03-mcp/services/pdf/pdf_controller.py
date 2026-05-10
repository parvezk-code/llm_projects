# services/pdf/pdf_controller.py

from services.pdf.pdf_service import PDFService
from app.models.services.pdf_document import PDFDocument
import os


class PDFLoadError(Exception):
    pass


class PDFController:

    def __init__(self, service: PDFService):
        self._service = service

    # --- Called by MainController ---

    def load(self, file_path: str) -> PDFDocument:
        try:
            full_text, page_count = self._service.extract_text(file_path)
            filename = os.path.basename(file_path)
            return PDFDocument(
                filename=filename,
                full_text=full_text,
                page_count=page_count
            )
        except Exception as e:
            raise PDFLoadError(
                f"Failed to load PDF — file may be corrupted or password-protected."
            ) from e