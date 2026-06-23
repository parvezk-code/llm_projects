# desktop/event_handlers/input_bar_event_handler.py

from desktop.action_bundles.action_bundle import ActionBundle
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.input_bar_controller import InputBarController


class InputBarEventHandler:
    """
    Handles events emitted by InputBarComponent.
    Organised by emitting component — one handler, one component.

    Constructor: (actions, chat_area, input_bar) — only what this handler needs.
    """

    def __init__(
        self,
        actions: ActionBundle,
        chat_area: ChatAreaController,
        input_bar: InputBarController,
    ) -> None:
        self._actions = actions
        self._chat_area = chat_area
        self._input_bar = input_bar

    def on_send_clicked(self) -> None:
        """Triggered by InputBarComponent.send_triggered signal."""
        user_text = self._input_bar.get_text()
        if not user_text:
            return

        self._input_bar.set_enabled(False)

        try:
            user_msg, assistant_msg = self._actions.send_message.execute(user_text)
            # Unpack domain models to primitives — UI never sees ChatMessage
            self._chat_area.add_bubble(role=user_msg.role, content=user_msg.content)
            self._chat_area.add_bubble(role=assistant_msg.role, content=assistant_msg.content)
            self._input_bar.clear_text()
        except Exception as e:
            # LLM failures → inline error bubble in the chat area
            self._chat_area.add_bubble(role="assistant", content=f"Error: {e}")
        finally:
            self._input_bar.set_enabled(True)

# desktop/event_handlers/input_bar_event_handler.py