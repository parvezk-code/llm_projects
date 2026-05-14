# app/event_handlers/chat/send_message_handler.py

import logging
from app.state.state_controller import StateController
from app.event_handlers.transformers.chain.history_transformer import convert_history
from app.event_handlers.business_logic.worker import Worker
from services.chain.request import ChainRequest
from services.service_bundle import ServiceBundle
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class SendMessageHandler:

    def __init__(
        self,
        state: StateController,
        ui: UIBundle,
        service: ServiceBundle,
    ) -> None:
        self._state = state
        self._ui = ui
        self._service = service
        self._retriever = None
        self._worker: Worker | None = None

    def set_retriever(self, retriever: object) -> None:
        self._retriever = retriever

    def handle(self) -> None:
        user_input = self._ui.input_bar.get_text().strip()
        if not user_input:
            return

        self._ui.input_bar.clear_text()
        self._set_ui_busy(True)
        self._ui.status_bar.hide()

        self._state.add_message(role="user", content=user_input)
        self._ui.chat_area.add_bubble(role="user", content=user_input)

        self._worker = Worker(
            method=self._run_chain,
            on_result=self._on_result_ready,
        )
        self._worker.start()

    def _run_chain(self):
        history = convert_history(self._state.get_messages()[:-1])
        request = ChainRequest(
            history=history,
            user_input=self._state.get_messages()[-1].content,
            retriever=self._retriever if self._state.has_project() else None,
        )
        response = self._service.chain_controller.run(request)
        return response

    def _on_result_ready(self, response) -> None:
        if not response.has_error():
            self._on_result(response.answer)
        else:
            self._on_error(response.error)

    def _on_result(self, answer: str) -> None:
        self._state.add_message(role="assistant", content=answer)
        self._ui.chat_area.add_bubble(role="assistant", content=answer)
        self._set_ui_busy(False)

    def _on_error(self, error: str) -> None:
        self._state.pop_last_message()
        self._ui.chat_area.clear_last_bubble()
        self._state.set_error(error)
        self._ui.status_bar.show_error(error)
        self._set_ui_busy(False)

    def _set_ui_busy(self, busy: bool) -> None:
        self._ui.input_bar.set_enabled(not busy)
        self._ui.toolbar.set_enabled(not busy)