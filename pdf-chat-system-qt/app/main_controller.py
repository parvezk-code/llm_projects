# app/main_controller.py

from PyQt6.QtWidgets import QMainWindow
from ui.ui_composer import UIComposer
from ui.ui_bundle import UIBundle
from services.service_composer import ServiceComposer
from services.service_bundle import ServiceBundle
from services.pdf.pdf_controller import PDFLoadError
from services.llm.llm_controller import LLMCallError
from app.models.services.chat_message import ChatMessage
from app.models.services.llm_transaction import LLMTransaction
from app.models.state.app_state import AppState


class MainController:

    def __init__(self, window: QMainWindow):

        # --- Build UI ---
        self._ui: UIBundle = UIComposer().build(window)

        # --- Build Services ---
        self._svc: ServiceBundle = ServiceComposer().build()

        # --- Initialize state ---
        self._state = AppState()

        # --- Bind signals to handlers ---
        self._bind_signals()

    # -------------------------------------------------------------------------
    # Signal Binding
    # -------------------------------------------------------------------------

    def _bind_signals(self):
        self._ui.toolbar.bind_upload_requested( self._on_upload_clicked )
        self._ui.toolbar.bind_clear_clicked( self._on_clear_clicked )
        self._ui.status_bar.bind_dismissed( self._on_status_bar_dismissed )
        self._ui.input_bar.bind_send_clicked( self._on_send_clicked )

    # -------------------------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------------------------

    def _on_upload_clicked(self):
        # E-01: open file picker
        file_path = self._ui.toolbar.open_file_picker()
        if file_path:
            self._load_pdf(file_path)

    def _load_pdf(self, file_path: str):
        # E-02: pdf_loaded
        try:
            pdf = self._svc.pdf.load(file_path)
        except PDFLoadError as e:
            self._on_pdf_load_failed(str(e))
            return

        # Update state
        self._state.pdf = pdf
        self._state.messages = []
        self._state.error = None

        # Update UI
        self._ui.toolbar.show_pdf(pdf)
        self._ui.status_bar.hide_error()
        self._ui.chat_area.clear_bubbles()
        self._ui.chat_area.show_placeholder() if not self._state.messages \
            else self._ui.chat_area.hide_placeholder()
        self._ui.chat_area.hide_placeholder()
        self._ui.input_bar.set_enabled(True)

    def _on_status_bar_dismissed(self):
        # E-03: status_bar_dismissed
        self._state.error = None
        self._ui.status_bar.hide_error()

    def _on_send_clicked(self):
        # E-04: message_send_requested

        # Step 1 — Read input
        text = self._ui.input_bar.get_text()
        if not text:
            self._on_empty_query()
            return

        # Step 2 — Create user ChatMessage
        user_message = ChatMessage(role="user", content=text)

        # Step 3-5 — Update state and UI for loading
        self._state.is_loading = True
        self._ui.chat_area.show_loading()
        self._ui.input_bar.set_enabled(False)

        # Step 6 — Build LLMTransaction and invoke LLM
        transaction = LLMTransaction(
            pdf_text=self._state.pdf.full_text,
            history=list(self._state.messages),
            user_message=user_message
        )

        try:
            transaction = self._svc.llm.ask(transaction)
        except LLMCallError as e:
            self._on_llm_call_failed(str(e))
            return

        # Steps 8-10 — Update state
        self._state.messages.append(transaction.user_message)
        self._state.messages.append(transaction.response)
        self._state.is_loading = False

        # Steps 11-15 — Update UI
        self._ui.chat_area.hide_loading()
        self._ui.chat_area.add_message_bubble(transaction.user_message)
        self._ui.chat_area.add_message_bubble(transaction.response)
        self._ui.input_bar.set_enabled(True)
        self._ui.input_bar.clear_input()

    def _on_clear_clicked(self):
        # E-05: chat_cleared
        self._state.messages = []
        self._state.error = None
        self._ui.chat_area.clear_bubbles()
        self._ui.chat_area.show_placeholder()
        self._ui.status_bar.hide_error()

    # -------------------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------------------

    def _on_pdf_load_failed(self, message: str):
        self._state.error = message
        self._ui.status_bar.show_error(message)
        self._ui.input_bar.set_enabled(False)

    def _on_llm_call_failed(self, message: str):
        self._state.is_loading = False
        self._state.error = message
        self._ui.chat_area.hide_loading()
        self._ui.chat_area.add_error_bubble(message)
        self._ui.input_bar.set_enabled(True)

    def _on_empty_query(self):
        self._ui.chat_area.add_error_bubble(
            "Please enter a question before sending.")