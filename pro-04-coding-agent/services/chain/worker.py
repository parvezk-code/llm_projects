import logging
from PyQt6.QtCore import QThread, pyqtSignal
from services.chain.chain_controller import ChainController
from services.chain.request import ChainRequest

logger = logging.getLogger(__name__)


class ChainWorker(QThread):
    """
    Runs ChainController.run() in a background thread so the PyQt6
    UI never freezes while waiting for the OpenAI API response.

    Signals
    -------
    result_ready(str)    — emitted when chain returns a successful answer
    error_occurred(str)  — emitted when chain returns an error

    Usage (in send_message_handler.py)
    -----------------------------------
        self._worker = ChainWorker(controller, request)
        self._worker.result_ready.connect(self._on_result)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()
    """

    result_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, controller: ChainController, request: ChainRequest) -> None:
        super().__init__()
        self._controller = controller
        self._request = request

    def run(self) -> None:
        """Called by QThread.start(). Runs in background thread."""
        logger.debug("ChainWorker starting")
        response = self._controller.run(self._request)

        if response.has_answer():
            logger.debug("ChainWorker — emitting result_ready")
            self.result_ready.emit(response.answer)
        else:
            logger.warning("ChainWorker — emitting error_occurred: %s", response.error)
            self.error_occurred.emit(response.error or "Unknown error")
