# desktop/main_controller.py

from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.state.app_state import AppState
from desktop.state_controller.state_controller import StateController
from desktop.actions.chat.send_plain_message_action import SendPlainMessageAction
from desktop.actions.chat.send_rag_message_action import SendRagMessageAction
from desktop.actions.chat.clear_chat_action import ClearChatAction
from desktop.actions.project.load_project_action import LoadProjectAction
from desktop.action_bundles.action_bundle import ActionBundle
from desktop.event_handlers.input_bar.send_router_handler import SendRouterHandler
from desktop.event_handlers.toolbar.clear_chat_handler import ClearChatHandler
from desktop.event_handlers.toolbar.load_project_handler import LoadProjectHandler
from desktop.event_handlers.folder_picker.folder_selected_handler import FolderSelectedHandler
from desktop.event_handlers.status_bar.dismiss_handler import DismissHandler
from ui.screen_manager import ScreenManager
from ui.style_manager import StyleManager


class MainController:
    """
    Application composition root.

    Receives ready-made Gateways from the launcher — never builds them or decides
    local vs remote mode. Creates state, actions, the UI, the style manager, and
    event handlers; wires every component signal to a handler method; applies the
    default theme. Contains no business logic and never manipulates widgets directly.

    Level 2: handlers are partitioned by component (one class per event). Each
    handler is stored as its own instance attribute to prevent garbage collection.
    The send flow uses a single router (SendRouterHandler.on_send) that reads the
    mode and dispatches — no re-wiring on mode change.
    """

    DEFAULT_THEME = "ocean_blue.qss"
    UNLOCK_LEVEL = 2

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
        self._unlock_level()
        self._show()

    # --- startup steps (one task each) ---

    def _create_state(self) -> None:
        self._state = AppState()
        self._state_controller = StateController(self._state)

    def _create_actions(self) -> None:
        sc = self._state_controller
        gw = self._gateways
        self._actions = ActionBundle(
            send_plain=SendPlainMessageAction(sc, gw),
            send_rag=SendRagMessageAction(sc, gw),
            clear_chat=ClearChatAction(sc, gw),
            load_project=LoadProjectAction(sc, gw),
        )

    def _create_ui(self) -> None:
        self._screen_manager = ScreenManager()
        self._ui = self._screen_manager.build()

    def _create_style(self) -> None:
        self._style_manager = StyleManager()

    def _create_event_handlers(self) -> None:
        ui = self._ui
        actions = self._actions

        # input_bar — send router (the one multi-method handler)
        self._send_router_handler = SendRouterHandler(
            actions, ui.input_bar, ui.chat_area, ui.status_bar, ui.toolbar,
        )

        # toolbar — one handler per event
        self._clear_chat_handler = ClearChatHandler(
            actions, ui.toolbar, ui.chat_area, ui.input_bar, ui.status_bar,
        )
        self._load_project_handler = LoadProjectHandler(ui.folder_picker)

        # folder_picker — one handler per event
        self._folder_selected_handler = FolderSelectedHandler(
            actions, ui.toolbar, ui.input_bar, ui.chat_area, ui.status_bar,
        )

        # status_bar — one handler per event
        self._dismiss_handler = DismissHandler(ui.status_bar)

    def _wire_events(self) -> None:
        ui = self._ui
        ui.input_bar.bind_send_triggered(self._send_router_handler.on_send)
        ui.toolbar.bind_clear_clicked(self._clear_chat_handler.on_clear_clicked)
        ui.toolbar.bind_load_project_clicked(self._load_project_handler.on_load_project_clicked)
        ui.folder_picker.bind_folder_selected(self._folder_selected_handler.on_folder_selected)
        ui.status_bar.bind_dismiss_clicked(self._dismiss_handler.on_dismissed)

    def _apply_default_theme(self) -> None:
        self._style_manager.apply_theme(self.DEFAULT_THEME)

    def _unlock_level(self) -> None:
        self._ui.toolbar.unlock_level(self.UNLOCK_LEVEL)

    def _show(self) -> None:
        self._screen_manager.show()

# desktop/main_controller.py