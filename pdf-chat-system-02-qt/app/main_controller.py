# app/main_controller.py

from PyQt6.QtWidgets import QMainWindow

from ui.ui_composer import UIComposer
from ui.ui_bundle import UIBundle
from services.service_composer import ServiceComposer
from services.service_bundle import ServiceBundle
from app.models.state.app_state import AppState

from app.event_handlers.pdf.upload_pdf_handler import UploadPDFHandler
from app.event_handlers.pdf.remove_pdf_handler import RemovePDFHandler
from app.event_handlers.chat.send_message_handler import SendMessageHandler
from app.event_handlers.chat.clear_chat_handler import ClearChatHandler
from app.event_handlers.ui.theme_changed_handler import ThemeChangedHandler


class MainController:

    def __init__(self, window: QMainWindow):
        self._ui: UIBundle = UIComposer().build(window)         # Build UI
        self._svc: ServiceBundle = ServiceComposer().build()    # Build Services
        self._state = AppState()                                # Initialize state
        self._init_handlers()                                   # Instantiate handlers
        self._bind_signals()                                    # Bind signals to handlers

    @property
    def ui(self) -> UIBundle:
        return self._ui

    # Check: if we can make UIBundle and ServiceBundle singleton so that we need pass it to other classes
    def _init_handlers(self):
        self._upload_pdf   = UploadPDFHandler(self._state, self._ui, self._svc)
        self._remove_pdf   = RemovePDFHandler(self._state, self._ui)
        self._send_message = SendMessageHandler(self._state, self._ui, self._svc)
        self._clear_chat   = ClearChatHandler(self._state, self._ui)
        self._theme        = ThemeChangedHandler(self._state, self._ui)

    # create a map where we have event names and its method to hendel it and we write a code that reads this map and bind events to the methohds
    def _bind_signals(self):
        self._ui.toolbar.bind_upload_requested(self._upload_pdf.on_upload_clicked)
        self._ui.toolbar.bind_clear_clicked(self._clear_chat.on_clear_clicked)
        self._ui.status_bar.bind_dismissed(self._on_status_bar_dismissed)
        self._ui.input_bar.bind_send_clicked(self._send_message.on_send_clicked)
        self._ui.file_picker.bind_pdf_selected(self._upload_pdf.on_pdf_selected)
        # self._ui.toolbar.bind_theme_changed(self._theme.on_theme_changed)

    # -------------------------------------------------------------------------
    # Inline handlers — only for signals too thin to warrant their own handler
    # -------------------------------------------------------------------------

    def _on_status_bar_dismissed(self):
        self._state.error = None
        self._ui.status_bar.hide_error()
