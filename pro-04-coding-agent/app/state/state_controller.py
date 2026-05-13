# app/state/state_controller.py

from app.state.app_state import AppState
from app.state.models.chat_message import ChatMessage


class StateController:

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

    def clear_history(self) -> None:
        self._state.messages.clear()

    def has_messages(self) -> bool:
        return len(self._state.messages) > 0

    # --- error ---

    def set_error(self, error: str) -> None:
        self._state.error = error

    def clear_error(self) -> None:
        self._state.error = None

    def get_error(self) -> str | None:
        return self._state.error

    # --- project ---

    def set_project_path(self, path: str) -> None:
        self._state.project_path = path

    def get_project_path(self) -> str | None:
        return self._state.project_path

    def has_project(self) -> bool:
        return self._state.project_path is not None

    def clear_project(self) -> None:
        self._state.project_path = None