# core_services/vector_stores/faiss/controller.py

import logging
from core_services.vector_stores.faiss.service import FAISSVectorStoreService
from core_services.vector_stores.faiss.request import FAISSVectorStoreRequest
from core_services.vector_stores.faiss.response import FAISSVectorStoreResponse

logger = logging.getLogger(__name__)


class FAISSVectorStoreController:

    def __init__(self, service: FAISSVectorStoreService) -> None:
        self._service = service

    def run(self, request: FAISSVectorStoreRequest) -> FAISSVectorStoreResponse:
        try:
            retriever = self._service.build_retriever(chunks=request.chunks)
            return FAISSVectorStoreResponse(retriever=retriever)
        except Exception as e:
            logger.error(f"FAISSVectorStoreController error: {e}")
            return FAISSVectorStoreResponse(retriever=None, error=str(e))