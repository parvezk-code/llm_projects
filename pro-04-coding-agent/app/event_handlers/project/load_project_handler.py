# app/event_handlers/project/load_project_handler.py

import logging
from app.state.state_controller import StateController
from app.event_handlers.chat.send_message_handler import SendMessageHandler
from services.retriever.pipeline.controller import RetrieverPipelineController
from services.retriever.pipeline.request import RetrieverPipelineRequest
from app.event_handlers.business_logic.project.retriever_pipeline_worker import RetrieverPipelineWorker
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class LoadProjectHandler:

    def __init__(
        self,
        state: StateController,
        ui: UIBundle,
        retriever_controller: RetrieverPipelineController,
        send_handler: SendMessageHandler,
    ) -> None:
        self._state = state
        self._ui = ui
        self._retriever_controller = retriever_controller
        self._send_handler = send_handler
        self._worker: RetrieverPipelineWorker | None = None

    def handle(self, project_path: str) -> None:
        logger.info(f"Loading project: {project_path}")
        self._ui.status_bar.hide()
        self._ui.toolbar.set_enabled(False)
        self._ui.input_bar.set_enabled(False)

        self._worker = RetrieverPipelineWorker(
            controller=self._retriever_controller,
            request=RetrieverPipelineRequest(project_path=project_path),
        )
        self._worker.retriever_ready.connect(self._on_retriever_ready)
        self._worker.error_occurred.connect(self._on_retriever_error)
        self._worker.start()

    def _on_retriever_ready(self, retriever: object) -> None:
        self._state.set_project_path(self._worker._request.project_path)
        self._send_handler.set_retriever(retriever)
        self._ui.toolbar.set_enabled(True)
        self._ui.input_bar.set_enabled(True)
        logger.info("Retriever ready. RAG mode active.")

    def _on_retriever_error(self, error: str) -> None:
        self._state.set_error(error)
        self._ui.status_bar.show_error(error)
        self._ui.toolbar.set_enabled(True)
        self._ui.input_bar.set_enabled(True)
        logger.error(f"Retriever pipeline failed: {error}")