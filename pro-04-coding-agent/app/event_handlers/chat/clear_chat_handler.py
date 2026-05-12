import logging
from app.models.state.app_state import AppState
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class ClearChatHandler:
    """
    Handles the Clear button click.

    Steps:
    1. Reset AppState.messages and AppState.error
    2. Clear chat area bubbles (shows placeholder)
    3. Hide status bar
    4. Disable input bar
    5. Disable Clear button
    """

    def __init__(self, state: AppState, ui: UIBundle) -> None:
        self._state = state
        self._ui = ui

    def handle(self) -> None:
        logger.debug("ClearChatHandler: clearing chat")

        # 1. Reset state
        self._state.messages.clear()
        self._state.error = None

        # 2. Clear UI
        self._ui.chat_area.clear()
        self._ui.status_bar.hide()
        self._ui.input_bar.set_enabled(True)
        self._ui.toolbar.set_clear_enabled(False)

        logger.debug("ClearChatHandler: done")
