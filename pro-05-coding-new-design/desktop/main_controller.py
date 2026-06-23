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


class MainController:
    """
    Single composition root. Creates and wires every object.
    Receives a ready-made GatewayBundle from the launcher — never builds gateways.
    Holds no business logic.

    Startup sequence:
      create_state → create_actions → create_ui → create_event_handlers
      → wire_events → show
    """

    def __init__(self, gateways: GatewayBundle) -> None:
        # --- state ---
        state = StateController(AppState())

        # --- actions ---
        actions = ActionBundle(
            send_message=SendMessageAction(state=state, gateways=gateways),
            clear_chat=ClearChatAction(state=state, gateways=gateways),
        )

        # --- ui ---
        self._screen = ScreenManager()
        ui = self._screen.build()

        # --- event handlers (stored as instance attrs to prevent garbage collection) ---
        self._input_bar_handler = InputBarEventHandler(
            actions=actions,
            input_bar=ui.input_bar,
            chat_area=ui.chat_area,
            status_bar=ui.status_bar,
            toolbar=ui.toolbar,
        )
        self._toolbar_handler = ToolbarEventHandler(
            actions=actions,
            toolbar=ui.toolbar,
            chat_area=ui.chat_area,
            status_bar=ui.status_bar,
            input_bar=ui.input_bar,
        )

        # --- wire signals to handler methods ---
        self._wire_events(ui, self._input_bar_handler, self._toolbar_handler, state)

    def _wire_events(self, ui, input_bar_handler, toolbar_handler, state) -> None:
        ui.input_bar.bind_send_triggered(input_bar_handler.handle_send)
        ui.toolbar.bind_clear_clicked(toolbar_handler.handle_clear)
        ui.toolbar.bind_mode_changed(toolbar_handler.handle_mode_changed)
        ui.toolbar.bind_mode_changed(state.set_mode)

    def show(self) -> None:
        self._screen.show()