# app/event_handlers/project/load_project_handler.py

import logging
from app.applications.application_bundle import ApplicationBundle
from app.utils.worker import Worker
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class LoadProjectHandler:

    def __init__(
        self,
        ui: UIBundle,
        app: ApplicationBundle,
    ) -> None:
        self._ui = ui
        self._app = app
        self._worker: Worker | None = None
        self._project_path: str = ""

    def handle(self, project_path: str) -> None:
        logger.info(f"Loading project: {project_path}")
        self._project_path = project_path
        self._ui.status_bar.hide()
        self._ui.toolbar.set_enabled(False)
        self._ui.input_bar.set_enabled(False)

        self._worker = Worker(
            method=self._execute,
            on_result=self._on_result_ready,
        )
        self._worker.start()

    def _execute(self):
        return self._app.load_project.execute(self._project_path)

    def _on_result_ready(self, response) -> None:
        if response.has_error():
            self._on_retriever_error(response.error)
        else:
            self._on_retriever_ready(response.retriever)

    def _on_retriever_ready(self, retriever: object) -> None:
        self._app.send_message.set_retriever(retriever)
        self._ui.toolbar.set_project_name(self._project_path.split("/")[-1])
        self._ui.toolbar.set_enabled(True)
        self._ui.input_bar.set_enabled(True)
        logger.info("Retriever ready. RAG mode active.")

    def _on_retriever_error(self, error: str) -> None:
        self._ui.status_bar.show_error(error)
        self._ui.toolbar.set_enabled(True)
        self._ui.input_bar.set_enabled(True)
        logger.error(f"Retriever pipeline failed: {error}")