# app/applications/load_project_command.py

from app.state.state_controller import StateController
from services.retriever.pipeline.request import RetrieverPipelineRequest
from services.retriever.pipeline.response import RetrieverPipelineResponse
from services.service_bundle import ServiceBundle


class LoadProjectCommand:

    def __init__(
        self,
        state: StateController,
        service: ServiceBundle,
    ) -> None:
        self._state = state
        self._service = service

    def execute(self, project_path: str) -> RetrieverPipelineResponse:
        response = self._service.retriever_controller.run(
            RetrieverPipelineRequest(project_path=project_path)
        )
        if not response.has_error():
            self._state.set_project_path(project_path)
        return response