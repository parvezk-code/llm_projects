# app/state/app_state.py

from dataclasses import dataclass, field
from app.state.models.chat_message import ChatMessage


@dataclass
class AppState:
    messages: list[ChatMessage] = field(default_factory=list)
    error: str | None = None
    project_path: str | None = None
    mode: str = "Simple"