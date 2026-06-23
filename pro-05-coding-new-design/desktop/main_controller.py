# desktop/main_controller.py

from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.state.app_state import AppState
from desktop.state_controller.state_controller import StateController
from desktop.actions.chat.send_message_action import SendMessageAction
from desktop.actions.chat.clear_chat_action import ClearChatAction
from desktop.action_bundles.action_bundle import ActionBundle
from desktop.event_handlers.input_bar_event_handler import InputBarEventHandler
from desktop.event_handlers.toolbar_event_handler import ToolbarEventHandler
from ui.screen_manager import ScreenManager
from ui.style_manager import StyleManager


class MainController:
    """
    Application composition root.

    Receives ready-made Gateways from the launcher — never builds them or
    decides local vs remote mode. Creates state, actions, the UI, the style
    manager, and event handlers; wires every component signal to a handler
    method; applies the default theme. Contains no business logic and never
    manipulates widgets directly.
    """

    DEFAULT_THEME = "ocean_blue.qss"

    def __init__(self, gateways: GatewayBundle) -> None:
        self._gateways = gateways

    # --- public entry point ---

    def start(self) -> None:
        self._create_state()
        self._create_actions()
        self._create_ui()
        self._create_style()
        self._create_event_handlers()
        self._wire_events()
        self._apply_default_theme()
        self._show()

    # --- startup steps (one task each) ---

    def _create_state(self) -> None:
        self._state = AppState()
        self._state_controller = StateController(self._state)

    def _create_actions(self) -> None:
        self._actions = ActionBundle(
            send_message=SendMessageAction(self._state_controller, self._gateways),
            clear_chat=ClearChatAction(self._state_controller, self._gateways),
        )

    def _create_ui(self) -> None:
        self._screen_manager = ScreenManager()
        self._ui = self._screen_manager.build()

    def _create_style(self) -> None:
        self._style_manager = StyleManager()

    def _create_event_handlers(self) -> None:
        ui = self._ui
        self._input_bar_handler = InputBarEventHandler(
            self._actions,
            ui.chat_area,
            ui.input_bar,
        )
        self._toolbar_handler = ToolbarEventHandler(
            self._actions,
            self._style_manager,
            ui.toolbar,
            ui.chat_area,
            ui.input_bar,
            ui.status_bar,
        )

    def _wire_events(self) -> None:
        ui = self._ui
        ui.input_bar.bind_send_triggered(self._input_bar_handler.on_send_clicked)
        ui.toolbar.bind_clear_clicked(self._toolbar_handler.on_clear_clicked)
        ui.toolbar.bind_mode_changed(self._toolbar_handler.on_theme_changed)

    def _apply_default_theme(self) -> None:
        self._style_manager.apply_theme(self.DEFAULT_THEME)

    def _show(self) -> None:
        self._screen_manager.show()

# desktop/main_controller.py