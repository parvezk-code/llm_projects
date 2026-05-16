# app/applications/run_graph_command.py

import logging
from app.state.state_controller import StateController
from services.service_bundle import ServiceBundle
from services.graph.request import GraphRequest
from services.graph.response import GraphResponse

logger = logging.getLogger(__name__)


class RunGraphCommand:

    def __init__(
        self,
        state: StateController,
        service: ServiceBundle,
    ) -> None:
        self._state = state
        self._service = service
        self._thread_id: str = "default"

    def execute(self, user_input: str) -> GraphResponse:
        project_path = self._state.get_project_path()

        if not project_path:
            return GraphResponse(error="No project loaded. Please load a project first.")

        request = GraphRequest(
            project_path=project_path,
            user_input=user_input,
            thread_id=self._thread_id,
        )

        response = self._service.graph_controller.run(request)

        if response.has_error():
            logger.error(f"RunGraphCommand error: {response.error}")
        else:
            self._state.add_message(role="assistant", content=response.report)

        return response