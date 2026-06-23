# desktop/state/app_state.py

from dataclasses import dataclass, field
from core.models.chat_message import ChatMessage


@dataclass
class AppState:
    """
    Holds all current application data.
    Plain fields only — no methods, no logic.
    """
    messages: list[ChatMessage] = field(default_factory=list)
    mode: str = "Simple"