# app/event_handlers/pdf/remove_pdf_handler.py

from app.models.state.app_state import AppState
from ui.ui_bundle import UIBundle


class RemovePDFHandler:

    def __init__(self, state: AppState, ui: UIBundle):
        self._state = state
        self._ui = ui

    def on_remove(self):
        self._state.pdf = None
        self._state.messages = []
        self._state.error = None

        self._ui.chat_area.emptyAllChats()
        self._ui.status_bar.hide_error()
        self._ui.toolbar.on_chat_cleared()
        self._ui.input_bar.disableInput()
