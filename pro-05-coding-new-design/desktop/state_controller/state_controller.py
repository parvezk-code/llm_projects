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

    # --- coarse event operations (one per event; compose the fine-grained ones) ---

    def add_message_on_send(self, user_msg: ChatMessage, assistant_msg: ChatMessage) -> None:
        """The send commit: append both turns together (atomic — only on success)."""
        self._state.messages.append(user_msg)
        self._state.messages.append(assistant_msg)

    def reset_on_clear_chat(self) -> None:
        """The clear event's state slice: drop chat, project, and index together."""
        self.clear_chat()
        self.clear_project()
        self.clear_index()

    def reset_on_project_loaded(self, path: str, index: ProjectIndex) -> None:
        """The load event's state slice: store project + index, start a fresh chat."""
        self.set_project_path(path)
        self.set_project_index(index)
        self.clear_chat()

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