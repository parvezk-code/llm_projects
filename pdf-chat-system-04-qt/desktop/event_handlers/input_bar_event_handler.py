# desktop/event_handlers/input_bar_event_handler.py

from desktop.action_bundles.action_bundle import ActionBundle


class InputBarEventHandler:
    """
    Handles events emitted by the input bar.

    Component controllers are injected (never imported) so this layer does not
    depend on the UI layer. Core models returned by Actions are unpacked into
    primitives here before reaching the controllers.
    """

    def __init__(
        self,
        actions: ActionBundle,
        chat_area_controller,    # ChatAreaController
        input_bar_controller,    # InputBarController
    ):
        self._actions = actions
        self._chat_area = chat_area_controller
        self._input_bar = input_bar_controller

    def on_send_clicked(self, text: str):
        self._input_bar.disable_input()
        try:
            user_message, assistant_message = self._actions.send_message.execute(text)
            # unpack Core models -> primitives (UI never sees ChatMessage)
            self._chat_area.add_message(user_message.role, user_message.content)
            self._chat_area.add_message(assistant_message.role, assistant_message.content)
            self._input_bar.clear_input()
        except Exception as error:
            self._chat_area.show_error(f"Could not get a response: {error}")
        finally:
            self._input_bar.enable_input()

# desktop/event_handlers/input_bar_event_handler.py