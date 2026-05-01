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
        self._ui: UIBundle = UIComposer().build(window)         # Build UI
        self._svc: ServiceBundle = ServiceComposer().build()    # Build Services
        self._state = AppState()                                # Initialize state
        self._bind_signals()                                    # Bind signals to handlers

    @property
    def ui(self) -> UIBundle:
        return self._ui

    # Bind all signals(events to controller methods)
    def _bind_signals(self):
        self._ui.toolbar.bind_upload_requested(self._on_upload_clicked)
        self._ui.toolbar.bind_clear_clicked(self._on_clear_clicked)
        self._ui.status_bar.bind_dismissed(self._on_status_bar_dismissed)
        self._ui.input_bar.bind_send_clicked(self._on_send_clicked)
        self._ui.file_picker.bind_pdf_selected(self._load_pdf)
        # self._ui.file_picker.bind_dialog_canceled(self._on_pdf_dialog_canceled)
        
        # theme_changed
        # self._ui.toolbar.bind_theme_changed()

    # -------------------------------------------------------------------------
    # Event Handlers
    # -------------------------------------------------------------------------

    def _on_upload_clicked(self):
        # Open file picker: user will select a pdf to chat
        self._ui.file_picker.open_pdf()

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
        self._ui.toolbar.on_pdf_loaded(pdf)
        self._ui.status_bar.hide_error()
        self._ui.chat_area.emptyAllChats()
        self._ui.input_bar.enableInput()

    def _on_status_bar_dismissed(self):
        # E-03: status_bar_dismissed
        self._state.error = None
        self._ui.status_bar.hide_error()

    def _on_send_clicked(self, text: str):
        # Create user ChatMessage
        user_message = ChatMessage(role="user", content=text)

        # Build LLMTransaction and invoke LLM
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

        # Update state
        self._state.messages.append(transaction.user_message)
        self._state.messages.append(transaction.response)

        # Update UI
        self._ui.chat_area.handleNewMessage(transaction.user_message, transaction.response)
        self._ui.toolbar.on_chat_updated()
        self._ui.input_bar.clear_input()

    def _on_clear_clicked(self):
        # E-05: chat_cleared
        self._state.messages = []
        self._state.error = None
        self._ui.chat_area.emptyAllChats()
        self._ui.status_bar.hide_error()
        self._ui.toolbar.on_chat_cleared()
        self._ui.input_bar.disableInput()

    # -------------------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------------------

    def _on_pdf_load_failed(self, message: str):
        self._state.error = message
        self._ui.status_bar.show_error(message)

    def _on_llm_call_failed(self, message: str):
        self._state.error = message
        # self._ui.chat_area.handleFailedLLMCall(message)
        self._ui.status_bar.show_error(message)
        self._ui.toolbar.on_llm_call_failed()