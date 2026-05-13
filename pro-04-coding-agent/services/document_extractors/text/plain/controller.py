# services/document_extractors/text/plain/controller.py

import logging
from services.document_extractors.text.plain.service import PlainTextExtractorService
from services.document_extractors.text.plain.request import PlainTextExtractorRequest
from services.document_extractors.text.plain.response import PlainTextExtractorResponse

logger = logging.getLogger(__name__)


class PlainTextExtractorController:

    def __init__(
        self,
        service: PlainTextExtractorService,
        allowed_extensions: list[str],
    ) -> None:
        self._service = service
        self._allowed_extensions = allowed_extensions

    def run(self, request: PlainTextExtractorRequest) -> PlainTextExtractorResponse:
        try:
            documents = self._service.extract(
                directory_path=request.directory_path,
                allowed_extensions=self._allowed_extensions,
            )
            return PlainTextExtractorResponse(documents=documents)
        except Exception as e:
            logger.error(f"PlainTextExtractorController error: {e}")
            return PlainTextExtractorResponse(documents=[], error=str(e))