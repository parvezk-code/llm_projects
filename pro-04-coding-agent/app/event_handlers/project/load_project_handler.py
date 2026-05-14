# app/event_handlers/project/load_project_handler.py

import logging
from app.state.state_controller import StateController
from app.event_handlers.chat.send_message_handler import SendMessageHandler
from app.event_handlers.business_logic.worker import Worker
from services.retriever.pipeline.request import RetrieverPipelineRequest
from ui.ui_bundle import UIBundle
from services.service_bundle import ServiceBundle

logger = logging.getLogger(__name__)


class LoadProjectHandler:

    def __init__(
        self,
        state: StateController,
        ui: UIBundle,
        service:ServiceBundle,
        send_handler: SendMessageHandler,
    ) -> None:
        self._state = state
        self._ui = ui
        self._service = service
        self._send_handler = send_handler
        self._worker: Worker | None = None
        self._project_path: str = ""

    def handle(self, project_path: str) -> None:
        logger.info(f"Loading project: {project_path}")
        self._project_path = project_path
        self._ui.status_bar.hide()
        self._ui.toolbar.set_enabled(False)
        self._ui.input_bar.set_enabled(False)

        self._worker = Worker(
            method=self._build_retriever,
            on_result=self._on_retriever_ready,
        )
        self._worker.start()

    def _build_retriever(self):
        return self._service.retriever_controller.run(
            RetrieverPipelineRequest(project_path=self._project_path)
        )

    def _on_retriever_ready(self, response) -> None:
        self._state.set_project_path(self._project_path)
        self._send_handler.set_retriever(response.retriever)
        self._ui.toolbar.set_project_name(self._project_path.split("/")[-1])
        self._ui.toolbar.set_enabled(True)
        self._ui.input_bar.set_enabled(True)
        logger.info("Retriever ready. RAG mode active.")