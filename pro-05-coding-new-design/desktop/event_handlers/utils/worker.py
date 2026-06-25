# desktop/event_handlers/utils/worker.py

from PyQt6.QtCore import QThread, pyqtSignal


class Worker(QThread):
    """
    Runs a synchronous method on a background thread and delivers the outcome
    back on the main (GUI) thread via Qt signals.

    Threading is an Event Handler concern (Actions stay synchronous). Because our
    Actions raise on failure rather than returning an error object, this Worker
    captures any exception and routes it to a separate on_error callback, so the
    handler's success/error branching still happens on the main thread.

    method:    zero-arg callable executed off-thread; its return value is the result.
    on_result: called on the main thread with the method's return value.
    on_error:  called on the main thread with the raised Exception.

    Keep a reference to the Worker (e.g. on the handler) until it finishes, or it
    will be garbage collected mid-run.
    """

    _result_ready = pyqtSignal(object)
    _error_raised = pyqtSignal(object)

    def __init__(self, method, on_result, on_error) -> None:
        super().__init__()
        self._method = method
        self._result_ready.connect(on_result)
        self._error_raised.connect(on_error)

    def run(self) -> None:
        try:
            result = self._method()
        except Exception as error:  # surface to main thread, don't crash the thread
            self._error_raised.emit(error)
            return
        self._result_ready.emit(result)

# desktop/event_handlers/utils/worker.py