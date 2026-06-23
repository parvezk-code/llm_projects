# desktop/state_controller/state_controller.py

from core.models.chat_message import ChatMessage
from desktop.state.app_state import AppState


class StateController:
    """
    The single access point for reading and writing AppState.
    No business logic — only state operations.
    Only Actions call this.
    """

    def __init__(self, state: AppState) -> None:
        self._state = state

    # --- chat ---

    def add_chat_message(self, message: ChatMessage) -> None:
        self._state.messages.append(message)

    def get_chat_messages(self) -> list[ChatMessage]:
        return list(self._state.messages)   # copy — callers cannot mutate internal state

    def remove_last_chat_message(self) -> ChatMessage | None:
        if self._state.messages:
            return self._state.messages.pop()
        return None

    def is_chat_empty(self) -> bool:
        return len(self._state.messages) == 0

    def clear_chat(self) -> None:
        self._state.messages.clear()

    # --- processing ---

    def set_processing(self, value: bool) -> None:
        self._state.is_processing = value

    def is_processing(self) -> bool:
        return self._state.is_processing

# desktop/state_controller/state_controller.py