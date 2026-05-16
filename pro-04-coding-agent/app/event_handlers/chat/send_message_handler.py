# app/event_handlers/chat/send_message_handler.py

import logging
from app.applications.application_bundle import ApplicationBundle
from app.utils.worker import Worker
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class SendMessageHandler:

    def __init__(
        self,
        ui: UIBundle,
        app: ApplicationBundle,
    ) -> None:
        self._ui = ui
        self._app = app
        self._worker: Worker | None = None
        self._user_input: str = ""

    def handle(self) -> None:
        user_input = self._ui.input_bar.get_text().strip()
        if not user_input:
            return

        self._user_input = user_input
        self._ui.input_bar.clear_text()
        self._set_ui_busy(True)
        self._ui.status_bar.hide()
        self._ui.chat_area.add_bubble(role="user", content=user_input)

        mode = self._ui.toolbar.get_mode()

        if mode == "Graph":
            self._worker = Worker(
                method=self._execute_graph,
                on_result=self._on_graph_result_ready,
            )
        else:
            self._worker = Worker(
                method=self._execute,
                on_result=self._on_result_ready,
            )
        self._worker.start()

    def _execute(self):
        return self._app.send_message.execute(self._user_input)

    def _execute_graph(self):
        return self._app.run_graph.execute(self._user_input)

    def _on_result_ready(self, response) -> None:
        if response.has_error():
            self._ui.chat_area.clear_last_bubble()
            self._ui.status_bar.show_error(response.error)
        else:
            self._ui.chat_area.add_bubble(role="assistant", content=response.answer)
        self._set_ui_busy(False)

    def _on_graph_result_ready(self, response) -> None:
        if response.has_error():
            self._ui.chat_area.clear_last_bubble()
            self._ui.status_bar.show_error(response.error)
        else:
            self._ui.chat_area.add_bubble(role="assistant", content=response.report)
        self._set_ui_busy(False)

    def _set_ui_busy(self, busy: bool) -> None:
        self._ui.input_bar.set_enabled(not busy)
        self._ui.toolbar.set_enabled(not busy)