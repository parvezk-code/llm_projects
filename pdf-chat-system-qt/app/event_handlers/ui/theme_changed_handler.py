# app/event_handlers/ui/theme_changed_handler.py

from app.models.state.app_state import AppState
from ui.ui_bundle import UIBundle


class ThemeChangedHandler:

    def __init__(self, state: AppState, ui: UIBundle):
        self._state = state
        self._ui = ui

    def on_theme_changed(self, theme_name: str):
        # TODO: apply theme to QApplication or stylesheet loader
        pass
