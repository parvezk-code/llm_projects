# desktop/event_handlers/toolbar_event_handler.py

from desktop.action_bundles.action_bundle import ActionBundle
from ui.style_manager import StyleManager
from ui.controllers.toolbar_controller import ToolbarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.input_bar_controller import InputBarController
from ui.controllers.status_bar_controller import StatusBarController


class ToolbarEventHandler:
    """
    Handles events emitted by ToolbarComponent: clear, mode_changed.
    Organised by emitting component — one handler, one component.
    """

    def __init__(
        self,
        actions: ActionBundle,
        style_manager: StyleManager,
        toolbar: ToolbarController,
        chat_area: ChatAreaController,
        input_bar: InputBarController,
        status_bar: StatusBarController,
    ) -> None:
        self._actions = actions
        self._style_manager = style_manager
        self._toolbar = toolbar
        self._chat_area = chat_area
        self._input_bar = input_bar
        self._status_bar = status_bar

    def on_clear_clicked(self) -> None:
        """Triggered by ToolbarComponent.clear_clicked signal."""
        self._actions.clear_chat.execute()
        self._chat_area.clear()
        self._status_bar.hide()
        self._input_bar.set_enabled(True)
        self._toolbar.set_clear_enabled(False)

    def on_theme_changed(self, filename: str) -> None:
        """Triggered by ToolbarComponent.mode_changed signal. Level 1: no-op."""
        pass

# desktop/event_handlers/toolbar_event_handler.py