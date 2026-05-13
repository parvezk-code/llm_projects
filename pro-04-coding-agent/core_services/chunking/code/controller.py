# core_services/chunking/code/controller.py

import logging
from core_services.chunking.code.service import CodeChunkingService
from core_services.chunking.code.request import CodeChunkingRequest
from core_services.chunking.code.response import CodeChunkingResponse

logger = logging.getLogger(__name__)


class CodeChunkingController:

    def __init__(
        self,
        service: CodeChunkingService,
        chunk_size: int,
        chunk_overlap: int,
    ) -> None:
        self._service = service
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

    def run(self, request: CodeChunkingRequest) -> CodeChunkingResponse:
        try:
            chunks = self._service.chunk(
                documents=request.documents,
                chunk_size=self._chunk_size,
                chunk_overlap=self._chunk_overlap,
            )
            return CodeChunkingResponse(chunks=chunks)
        except Exception as e:
            logger.error(f"CodeChunkingController error: {e}")
            return CodeChunkingResponse(chunks=[], error=str(e))