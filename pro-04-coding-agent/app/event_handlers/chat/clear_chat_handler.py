# app/event_handlers/chat/clear_chat_handler.py

import logging
from app.applications.application_bundle import ApplicationBundle
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class ClearChatHandler:

    def __init__(
        self,
        ui: UIBundle,
        app: ApplicationBundle,
    ) -> None:
        self._ui = ui
        self._app = app

    def handle(self) -> None:
        logger.debug("ClearChatHandler: clearing chat")

        self._app.clear_chat.execute()

        self._ui.chat_area.clear()
        self._ui.status_bar.hide()
        self._ui.input_bar.set_enabled(True)
        self._ui.toolbar.set_clear_enabled(False)
        self._ui.toolbar.clear_project_label()

        logger.debug("ClearChatHandler: done")