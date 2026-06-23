# desktop/event_handlers/toolbar_event_handler.py

from desktop.action_bundles.action_bundle import ActionBundle
from ui.controllers.toolbar_controller import ToolbarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.status_bar_controller import StatusBarController
from ui.controllers.input_bar_controller import InputBarController

class ToolbarEventHandler:
    """
    Handles events emitted by the ToolbarComponent.
    Organised by emitting component — one handler, one component.

    Injected controllers:
      - toolbar: update label, enable/disable
      - chat_area: clear bubbles
      - status_bar: hide on clear
      - input_bar: re-enable after clear
    """

    def __init__(
        self,
        actions: ActionBundle,
        toolbar: ToolbarController,
        chat_area: ChatAreaController,
        status_bar: StatusBarController,
        input_bar: InputBarController,
    ) -> None:
        self._actions = actions
        self._toolbar = toolbar
        self._chat_area = chat_area
        self._status_bar = status_bar
        self._input_bar = input_bar

    def handle_clear(self) -> None:
        """Triggered by ToolbarComponent.clear_clicked signal."""
        self._actions.clear_chat.execute()

        self._chat_area.clear()
        self._status_bar.hide()
        self._input_bar.set_enabled(True)
        self._toolbar.set_clear_enabled(False)

    def handle_mode_changed(self, mode: str) -> None:
        """Triggered by ToolbarComponent.mode_changed signal. Level 1: Simple only."""
        # mode is a primitive string — no unpacking needed
        # StateController is updated via direct binding in MainController (see doc_04 rules)