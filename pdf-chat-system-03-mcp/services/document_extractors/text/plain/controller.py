# services/document_extractors/text/plain/controller.py

from services.document_extractors.text.plain.service import PlainTextService
from services.document_extractors.text.plain.request import PlainTextRequest
from services.document_extractors.text.plain.response import PlainTextResponse


class PlainTextController:

    def __init__(self, service: PlainTextService):
        self._service = service

    # --- Called by MainController ---

    def extract(self, request: PlainTextRequest) -> PlainTextResponse:
        try:
            full_text = self._service.extract_text(request.file_path)
            return PlainTextResponse(
                full_text=full_text
            )
        except Exception as e:
            return PlainTextResponse(
                error=f"Failed to read text file — file may be missing or unreadable."
            )
