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

    # --- messages ---

    def add_message(self, role: str, content: str) -> None:
        self._state.messages.append(ChatMessage(role=role, content=content))

    def get_messages(self) -> list[ChatMessage]:
        return list(self._state.messages)

    def pop_last_message(self) -> ChatMessage | None:
        if self._state.messages:
            return self._state.messages.pop()
        return None

    def clear_messages(self) -> None:
        self._state.messages.clear()

    def has_messages(self) -> bool:
        return len(self._state.messages) > 0

    # --- mode ---

    def set_mode(self, mode: str) -> None:
        self._state.mode = mode

    def get_mode(self) -> str:
        return self._state.mode