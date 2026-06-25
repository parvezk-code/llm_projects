# desktop/state_controller/state_controller.py

from core.models.chat_message import ChatMessage
from core.models.project_index import ProjectIndex
from desktop.state.app_state import AppState


class StateController:
    """
    The single access point for reading and writing AppState.
    No business logic — only state operations.
    Only Actions call this.

    Level 2: mode accessors removed; project + index accessors added.
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

    # --- project ---

    def set_project_path(self, path: str) -> None:
        self._state.project_path = path

    def get_project_path(self) -> str | None:
        return self._state.project_path

    def has_project(self) -> bool:
        return self._state.project_path is not None

    def clear_project(self) -> None:
        self._state.project_path = None

    # --- project index ---

    def set_project_index(self, index: ProjectIndex) -> None:
        self._state.project_index = index

    def get_project_index(self) -> ProjectIndex | None:
        return self._state.project_index

    def has_index(self) -> bool:
        return self._state.project_index is not None

    def clear_index(self) -> None:
        self._state.project_index = None

# desktop/state_controller/state_controller.py