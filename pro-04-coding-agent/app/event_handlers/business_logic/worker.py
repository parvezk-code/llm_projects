# app/event_handlers/business_logic/worker.py

from PyQt6.QtCore import QThread, pyqtSignal


class Worker(QThread):
    result_ready = pyqtSignal(object)

    def __init__(self, method, on_result) -> None:
        super().__init__()
        self._method = method
        self.result_ready.connect(on_result)

    def run(self) -> None:
        response = self._method()
        self.result_ready.emit(response)