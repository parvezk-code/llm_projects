# app/event_handlers/chat/clear_chat_handler.py

import logging
from app.state.state_controller import StateController
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class ClearChatHandler:
    """
    Handles the Clear button click.

    Steps:
    1. Reset messages and error via StateController
    2. Clear chat area bubbles (shows placeholder)
    3. Hide status bar
    4. Disable input bar
    5. Disable Clear button
    """

    def __init__(self, state: StateController, ui: UIBundle) -> None:
        self._state = state
        self._ui = ui

    def handle(self) -> None:
        logger.debug("ClearChatHandler: clearing chat")

        # ── 1. Reset state ────────────────────────────────────────────────────
        self._state.clear_history()
        self._state.clear_error()

        # ── 2. Clear UI ───────────────────────────────────────────────────────
        self._ui.chat_area.clear()
        self._ui.status_bar.hide()
        self._ui.input_bar.set_enabled(True)
        self._ui.toolbar.set_clear_enabled(False)

        logger.debug("ClearChatHandler: done")