# app/state/state_controller.py

import logging
from app.state.app_state import AppState
from app.state.models.chat_message import ChatMessage

logger = logging.getLogger(__name__)


class StateController:
    """
    Owns all reads and writes to AppState.
    No other component should mutate AppState directly.

    Passed by reference to event handlers in place of raw AppState.
    """

    def __init__(self, state: AppState) -> None:
        self._state = state

    # ── Messages ─────────────────────────────────────────────────────────────

    def add_message(self, role: str, content: str) -> None:
        """Append a new ChatMessage to history."""
        self._state.messages.append(ChatMessage(role=role, content=content))
        logger.debug("StateController: added message role='%s'", role)

    def get_messages(self) -> list[ChatMessage]:
        """Return a shallow copy of the message history."""
        return list(self._state.messages)

    def pop_last_message(self) -> ChatMessage | None:
        """
        Remove and return the last message.
        Returns None if history is empty.
        Used to roll back a user message when a chain turn fails.
        """
        if self._state.messages:
            msg = self._state.messages.pop()
            logger.debug("StateController: popped message role='%s'", msg.role)
            return msg
        return None

    def clear_history(self) -> None:
        """Wipe all messages from history."""
        self._state.messages.clear()
        logger.debug("StateController: history cleared")

    def has_messages(self) -> bool:
        """Return True if there is at least one message in history."""
        return bool(self._state.messages)

    # ── Error ─────────────────────────────────────────────────────────────────

    def set_error(self, message: str) -> None:
        """Store an error string on state."""
        self._state.error = message
        logger.debug("StateController: error set")

    def clear_error(self) -> None:
        """Clear any stored error."""
        self._state.error = None

    def get_error(self) -> str | None:
        """Return the current error string, or None if no error."""
        return self._state.error