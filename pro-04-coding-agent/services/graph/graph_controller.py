# services/graph/graph_controller.py

import logging
from services.graph.graph_service import GraphService
from services.graph.request import GraphRequest
from services.graph.response import GraphResponse

logger = logging.getLogger(__name__)


class GraphController:

    def __init__(self, service: GraphService) -> None:
        self._service = service

    def run(self, request: GraphRequest) -> GraphResponse:
        try:
            report = self._service.run(
                project_path=request.project_path,
                user_input=request.user_input,
                thread_id=request.thread_id,
            )
            return GraphResponse(report=report)
        except Exception as e:
            logger.error(f"GraphController error: {e}")
            return GraphResponse(error=str(e))