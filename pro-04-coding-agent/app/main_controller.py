import logging
from PyQt6.QtWidgets import QMainWindow
from app.models.state.app_state import AppState
from app.event_handlers.chat.send_message_handler import SendMessageHandler
from app.event_handlers.chat.clear_chat_handler import ClearChatHandler
from conf.settings.config_bundle import ConfigBundle
from services.service_bundle import ServiceBundle
from services.service_composer import ServiceComposer
from ui.ui_bundle import UIBundle
from ui.ui_composer import UIComposer

logger = logging.getLogger(__name__)


class MainController:
    """
    Slim orchestrator. Owns AppState.
    Builds UI and services. Instantiates event handlers.
    Wires all signals to handlers via _bind_signals().
    """

    def __init__(self, window: QMainWindow, config: ConfigBundle) -> None:
        self._window = window
        self._config = config

        # ── State ─────────────────────────────────────────────────────────────
        self._state = AppState()

        # ── UI ────────────────────────────────────────────────────────────────
        self._ui: UIBundle = UIComposer.compose(window)

        # ── Services ──────────────────────────────────────────────────────────
        self._services: ServiceBundle = ServiceComposer.compose(config)

        # ── Event handlers ────────────────────────────────────────────────────
        self._send_handler = SendMessageHandler(
            state=self._state,
            ui=self._ui,
            services=self._services,
            system_prompt=config.app.system_prompt,
        )
        self._clear_handler = ClearChatHandler(
            state=self._state,
            ui=self._ui,
        )

        # ── Signals ───────────────────────────────────────────────────────────
        self._bind_signals()

        logger.debug("MainController: initialised")

    def _bind_signals(self) -> None:
        self._ui.input_bar.send_clicked.connect(self._send_handler.handle)
        self._ui.toolbar.clear_clicked.connect(self._clear_handler.handle)
