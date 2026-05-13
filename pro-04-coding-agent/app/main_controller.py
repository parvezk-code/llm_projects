# app/main_controller.py

import logging
from PyQt6.QtWidgets import QMainWindow

from conf.settings.config_bundle import ConfigBundle
from app.state.app_state import AppState
from app.state.state_controller import StateController
from app.event_handlers.chat.send_message_handler import SendMessageHandler
from app.event_handlers.chat.clear_chat_handler import ClearChatHandler
from app.event_handlers.project.load_project_handler import LoadProjectHandler
from services.service_composer import ServiceComposer
from services.service_bundle import ServiceBundle
from ui.ui_composer import UIComposer
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class MainController:

    def __init__(self, window: QMainWindow, config: ConfigBundle) -> None:
        self._window = window

        # --- state ---
        self._state = StateController(AppState())

        # --- services ---
        self._service_bundle: ServiceBundle = ServiceComposer(config=config).compose()

        # --- ui ---
        self._ui_bundle: UIBundle = UIComposer().compose(window=self._window)

        # --- event handlers ---
        self._send_handler = SendMessageHandler(
            state=self._state,
            ui=self._ui_bundle,
            service=self._service_bundle,
        )
        self._clear_handler = ClearChatHandler(
            state=self._state,
            ui=self._ui_bundle,
        )
        self._load_project_handler = LoadProjectHandler(
            state=self._state,
            ui=self._ui_bundle,
            retriever_controller=self._service_bundle.retriever_controller,
            send_handler=self._send_handler,
        )

        self._bind_signals()

    def _bind_signals(self) -> None:
        self._ui_bundle.input_bar.send_clicked.connect(self._send_handler.handle)
        self._ui_bundle.toolbar.clear_clicked.connect(self._clear_handler.handle)
        self._ui_bundle.toolbar.project_loaded.connect(self._load_project_handler.handle)