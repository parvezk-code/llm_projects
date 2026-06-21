# desktop/main_controller.py

from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.state.app_state import AppState
from desktop.state_controller.state_controller import StateController
from desktop.actions.chat.send_message_action import SendMessageAction
from desktop.actions.chat.clear_chat_action import ClearChatAction
from desktop.actions.document.upload_document_action import UploadDocumentAction
from desktop.action_bundles.action_bundle import ActionBundle
from desktop.event_handlers.toolbar_event_handler import ToolbarEventHandler
from desktop.event_handlers.input_bar_event_handler import InputBarEventHandler
from desktop.event_handlers.status_bar_event_handler import StatusBarEventHandler
from desktop.event_handlers.file_picker_event_handler import FilePickerEventHandler
from ui.screen_manager import ScreenManager
from ui.style_manager import StyleManager


class MainController:
    """
    Application composition root.

    Receives ready-made Gateways from the launcher (it never builds them and
    never decides local vs remote mode). It creates state, actions, the UI,
    the style manager, and the event handlers, then wires every component
    signal to a handler method and applies the default theme. It contains no
    business logic and never manipulates widgets directly.
    """

    DEFAULT_THEME = "theme_01_slate_indigo.qss"

    def __init__(self, gateways: GatewayBundle, screen: str = "main"):
        self._gateways = gateways
        self._screen = screen

    # --- Startup sequence ---

    def start(self):
        self._create_state()
        self._create_actions()
        self._create_ui()
        self._create_style()
        self._create_event_handlers()
        self._wire_events()
        self._apply_default_theme()
        self._show()

    # --- Steps (one task each) ---

    def _create_state(self):
        self._state = AppState()
        self._state_controller = StateController(self._state)

    def _create_actions(self):
        state_controller = self._state_controller
        gateways = self._gateways
        self._actions = ActionBundle(
            send_message=SendMessageAction(state_controller, gateways),
            clear_chat=ClearChatAction(state_controller, gateways),
            upload_document=UploadDocumentAction(state_controller, gateways),
        )

    def _create_ui(self):
        self._screen_manager = ScreenManager(screen=self._screen)
        self._ui = self._screen_manager.build()   # UIBundle of controllers

    def _create_style(self):
        self._style_manager = StyleManager()

    def _create_event_handlers(self):
        ui = self._ui
        actions = self._actions
        self._toolbar_handler = ToolbarEventHandler(
            actions, self._style_manager,
            ui.file_picker, ui.toolbar, ui.chat_area, ui.input_bar, ui.status_bar,
        )
        self._input_bar_handler = InputBarEventHandler(
            actions, ui.chat_area, ui.input_bar,
        )
        self._status_bar_handler = StatusBarEventHandler(ui.status_bar)
        self._file_picker_handler = FilePickerEventHandler(
            actions, ui.toolbar, ui.input_bar, ui.chat_area, ui.status_bar,
        )

    def _wire_events(self):
        ui = self._ui

        ui.toolbar.bind_upload_requested(self._toolbar_handler.on_upload_clicked)
        ui.toolbar.bind_clear_clicked(self._toolbar_handler.on_clear_clicked)
        ui.toolbar.bind_theme_changed(self._toolbar_handler.on_theme_changed)

        ui.input_bar.bind_send_clicked(self._input_bar_handler.on_send_clicked)

        ui.status_bar.bind_dismissed(self._status_bar_handler.on_dismissed)

        ui.file_picker.bind_pdf_selected(self._file_picker_handler.on_pdf_selected)
        ui.file_picker.bind_dialog_canceled(self._file_picker_handler.on_dialog_canceled)

    def _apply_default_theme(self):
        self._style_manager.apply_theme(self.DEFAULT_THEME)

    def _show(self):
        self._screen_manager.show()

# desktop/main_controller.py