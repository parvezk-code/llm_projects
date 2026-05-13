# services/retriever/pipeline/controller.py

import logging
from services.retriever.pipeline.service import RetrieverPipelineService
from services.retriever.pipeline.request import RetrieverPipelineRequest
from services.retriever.pipeline.response import RetrieverPipelineResponse

logger = logging.getLogger(__name__)


class RetrieverPipelineController:

    def __init__(self, service: RetrieverPipelineService) -> None:
        self._service = service

    def run(self, request: RetrieverPipelineRequest) -> RetrieverPipelineResponse:
        try:
            retriever = self._service.build(project_path=request.project_path)
            return RetrieverPipelineResponse(retriever=retriever)
        except Exception as e:
            logger.error(f"RetrieverPipelineController error: {e}")
            return RetrieverPipelineResponse(retriever=None, error=str(e))