# app/event_handlers/chat/send_message_handler.py

from services.llm.llm_controller import LLMCallError
from app.models.services.chat_message import ChatMessage
from app.models.services.llm_transaction import LLMTransaction
from app.models.state.app_state import AppState
from ui.ui_bundle import UIBundle
from services.service_bundle import ServiceBundle


class SendMessageHandler:

    def __init__(self, state: AppState, ui: UIBundle, svc: ServiceBundle):
        self._state = state
        self._ui = ui
        self._svc = svc

    def on_send_clicked(self, text: str):
        user_message = ChatMessage(role="user", content=text)

        transaction = LLMTransaction(
            pdf_text=self._state.pdf.full_text,
            history=list(self._state.messages),
            user_message=user_message
        )

        try:
            transaction = self._svc.llm.ask(transaction)
        except LLMCallError as e:
            self._on_llm_failed(str(e))
            return

        self._state.messages.append(transaction.user_message)
        self._state.messages.append(transaction.response)

        self._ui.chat_area.handleNewMessage(transaction.user_message, transaction.response)
        self._ui.toolbar.on_chat_updated()
        self._ui.input_bar.clear_input()

    def _on_llm_failed(self, message: str):
        self._state.error = message
        self._ui.status_bar.show_error(message)
        self._ui.toolbar.on_llm_call_failed()
