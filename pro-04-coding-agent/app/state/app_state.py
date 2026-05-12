# app/state_controller.py

from dataclasses import dataclass, field
from app.state.models.chat_message import ChatMessage


@dataclass
class AppState:
    """
    Central mutable state owned by MainController.
    Passed by reference to all event handlers.

    messages: full conversation history as ChatMessage list
    error: last error string, or None if no error
    """
    messages: list[ChatMessage] = field(default_factory=list)
    error: str | None = None
