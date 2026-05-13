# app/main_controller.py

import logging
from PyQt6.QtWidgets import QMainWindow

from conf.settings.config_bundle import ConfigBundle
from app.state.app_state import AppState
from app.state.state_controller import StateController
from app.event_handlers.chat.send_message_handler import SendMessageHandler
from app.event_handlers.chat.clear_chat_handler import ClearChatHandler
from services.service_composer import ServiceComposer
from services.service_bundle import ServiceBundle
from services.retriever.pipeline.request import RetrieverPipelineRequest
from services.retriever.pipeline.worker import RetrieverPipelineWorker
from ui.ui_composer import UIComposer
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class MainController:

    def __init__(self, window: QMainWindow, config: ConfigBundle) -> None:
        self._window = window

        # --- state ---
        self._state = StateController(AppState())

        # --- services ---
        self._service_bundle: ServiceBundle = ServiceComposer(config=config).compose()

        # --- ui ---
        self._ui_bundle: UIBundle = UIComposer().compose(window=self._window)
        # --- event handlers ---
        self._send_handler = SendMessageHandler(
            state=self._state,
            ui=self._ui_bundle,
            service=self._service_bundle,
        )
        self._clear_handler = ClearChatHandler(
            state=self._state,
            ui=self._ui_bundle,
        )

        self._retriever_worker: RetrieverPipelineWorker | None = None

        self._bind_signals()

    def _bind_signals(self) -> None:
        self._ui_bundle.input_bar.send_clicked.connect(self._send_handler.handle)
        self._ui_bundle.toolbar.clear_clicked.connect(self._clear_handler.handle)
        self._ui_bundle.toolbar.project_loaded.connect(self._on_project_loaded)

    def _on_project_loaded(self, project_path: str) -> None:
        logger.info(f"Loading project: {project_path}")
        self._ui_bundle.status_bar.hide()
        self._ui_bundle.toolbar.set_enabled(False)
        self._ui_bundle.input_bar.set_enabled(False)

        self._retriever_worker = RetrieverPipelineWorker(
            controller=self._service_bundle.retriever_controller,
            request=RetrieverPipelineRequest(project_path=project_path),
        )
        self._retriever_worker.retriever_ready.connect(self._on_retriever_ready)
        self._retriever_worker.error_occurred.connect(self._on_retriever_error)
        self._retriever_worker.start()

    def _on_retriever_ready(self, retriever: object) -> None:
        self._state.set_project_path(self._retriever_worker._request.project_path)
        self._send_handler.set_retriever(retriever)
        self._ui_bundle.toolbar.set_enabled(True)
        self._ui_bundle.input_bar.set_enabled(True)
        logger.info("Retriever ready. RAG mode active.")

    def _on_retriever_error(self, error: str) -> None:
        self._state.set_error(error)
        self._ui_bundle.status_bar.show_error(error)
        self._ui_bundle.toolbar.set_enabled(True)
        self._ui_bundle.input_bar.set_enabled(True)
        logger.error(f"Retriever pipeline failed: {error}")