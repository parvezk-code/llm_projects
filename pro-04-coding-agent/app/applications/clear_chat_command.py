# app/applications/clear_chat_command.py

from app.state.state_controller import StateController


class ClearChatCommand:

    def __init__(self, state: StateController) -> None:
        self._state = state

    def execute(self) -> None:
        self._state.clear_history()
        self._state.clear_error()
        self._state.clear_project()