# services/embedding_generators/openai/controller.py

import logging
from services.embedding_generators.openai.service import OpenAIEmbeddingService
from services.embedding_generators.openai.request import OpenAIEmbeddingRequest
from services.embedding_generators.openai.response import OpenAIEmbeddingResponse

logger = logging.getLogger(__name__)


class OpenAIEmbeddingController:

    def __init__(self, service: OpenAIEmbeddingService) -> None:
        self._service = service

    def run(self, request: OpenAIEmbeddingRequest) -> OpenAIEmbeddingResponse:
        try:
            embeddings = self._service.embed(chunks=request.chunks)
            return OpenAIEmbeddingResponse(embeddings=embeddings)
        except Exception as e:
            logger.error(f"OpenAIEmbeddingController error: {e}")
            return OpenAIEmbeddingResponse(embeddings=[], error=str(e))