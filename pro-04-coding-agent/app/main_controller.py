# app/main_controller.py

import logging
from PyQt6.QtWidgets import QMainWindow

from conf.settings.config_bundle import ConfigBundle
from app.state.app_state import AppState
from app.state.state_controller import StateController
from app.applications.send_message_command import SendMessageCommand
from app.applications.clear_chat_command import ClearChatCommand
from app.applications.load_project_command import LoadProjectCommand
from app.applications.application_bundle import ApplicationBundle
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

        # --- applications ---
        self._app_bundle = ApplicationBundle(
            send_message=SendMessageCommand(
                state=self._state,
                service=self._service_bundle,
            ),
            clear_chat=ClearChatCommand(
                state=self._state,
            ),
            load_project=LoadProjectCommand(
                state=self._state,
                service=self._service_bundle,
            ),
        )

        # --- event handlers ---
        self._send_handler = SendMessageHandler(
            ui=self._ui_bundle,
            app=self._app_bundle,
        )
        self._clear_handler = ClearChatHandler(
            ui=self._ui_bundle,
            app=self._app_bundle,
        )
        self._load_project_handler = LoadProjectHandler(
            ui=self._ui_bundle,
            app=self._app_bundle,
        )

        self._bind_signals()

    def _bind_signals(self) -> None:
        self._ui_bundle.input_bar.bind_send_clicked(self._send_handler.handle)
        self._ui_bundle.toolbar.bind_clear_clicked(self._clear_handler.handle)
        self._ui_bundle.toolbar.bind_load_project_clicked(self._ui_bundle.folder_picker.open)
        self._ui_bundle.folder_picker.bind_folder_selected(self._load_project_handler.handle)
        self._ui_bundle.toolbar.bind_mode_changed(self._state.set_mode)