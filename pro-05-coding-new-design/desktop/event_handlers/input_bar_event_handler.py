# desktop/event_handlers/input_bar_event_handler.py

from desktop.action_bundles.action_bundle import ActionBundle
from ui.controllers.input_bar_controller import InputBarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.status_bar_controller import StatusBarController
from ui.controllers.toolbar_controller import ToolbarController


class InputBarEventHandler:
    """
    Handles events emitted by the InputBarComponent.
    Organised by emitting component — one handler, one component.

    Injected controllers (never imported UI layer directly):
      - input_bar: read text, clear, enable/disable
      - chat_area: add/remove bubbles
      - status_bar: show/hide errors
      - toolbar: enable/disable during busy state
    """

    def __init__(
        self,
        actions: ActionBundle,
        input_bar: InputBarController,
        chat_area: ChatAreaController,
        status_bar: StatusBarController,
        toolbar: ToolbarController,
    ) -> None:
        self._actions = actions
        self._input_bar = input_bar
        self._chat_area = chat_area
        self._status_bar = status_bar
        self._toolbar = toolbar

    def handle_send(self) -> None:
        """Triggered by InputBarComponent.send_triggered signal."""
        user_input = self._input_bar.get_text()
        if not user_input:
            return

        self._input_bar.clear_text()
        self._status_bar.hide()
        self._set_busy(True)
        self._chat_area.add_bubble(role="user", content=user_input)

        try:
            answer = self._actions.send_message.execute(user_input)
            self._chat_area.add_bubble(role="assistant", content=answer)
        except Exception as e:
            self._chat_area.clear_last_bubble()
            self._status_bar.show_error(str(e))
        finally:
            self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        self._input_bar.set_enabled(not busy)
        self._toolbar.set_enabled(not busy)