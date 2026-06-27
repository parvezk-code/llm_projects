# desktop/event_handlers/toolbar/clear_chat_handler.py

from desktop.action_bundles.action_bundle import ActionBundle
from ui.controllers.toolbar_controller import ToolbarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.input_bar_controller import InputBarController
from ui.controllers.status_bar_controller import StatusBarController


class ClearChatHandler:
    """
    Handles ToolbarComponent.clear_clicked.
    Resets the session: clears chat + project + index (via action), then resets
    the UI surfaces.
    """

    def __init__(
        self,
        actions: ActionBundle,
        toolbar: ToolbarController,
        chat_area: ChatAreaController,
        input_bar: InputBarController,
        status_bar: StatusBarController,
    ) -> None:
        self._actions = actions
        self._toolbar = toolbar
        self._chat_area = chat_area
        self._input_bar = input_bar
        self._status_bar = status_bar

    def on_clear_clicked(self) -> None:
        self._actions.clear_chat.execute()
        self._chat_area.reset_on_clear_chat()
        self._status_bar.reset_on_clear_chat()
        self._input_bar.reset_on_clear_chat()
        self._toolbar.reset_on_clear_chat()

# desktop/event_handlers/toolbar/clear_chat_handler.py