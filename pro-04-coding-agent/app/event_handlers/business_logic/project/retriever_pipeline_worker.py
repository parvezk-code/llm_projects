# app/event_handlers/business_logic/project/retriever_pipeline_worker.py

import logging
from PyQt6.QtCore import QThread, pyqtSignal

from services.retriever.pipeline.controller import RetrieverPipelineController
from services.retriever.pipeline.request import RetrieverPipelineRequest

logger = logging.getLogger(__name__)


class RetrieverPipelineWorker(QThread):
    retriever_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)

    def __init__(
        self,
        controller: RetrieverPipelineController,
        request: RetrieverPipelineRequest,
    ) -> None:
        super().__init__()
        self._controller = controller
        self._request = request

    def run(self) -> None:
        logger.info("RetrieverPipelineWorker started.")
        response = self._controller.run(self._request)
        if response.has_error():
            self.error_occurred.emit(response.error)
        else:
            self.retriever_ready.emit(response.retriever)