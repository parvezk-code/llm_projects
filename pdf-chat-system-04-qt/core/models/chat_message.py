# core/models/chat_message.py

from dataclasses import dataclass


class Role:
    """The allowed chat roles, named in one place to avoid stray string literals."""

    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class ChatMessage:
    """A single turn in the conversation. role is Role.USER or Role.ASSISTANT."""

    role: str
    content: str

    @classmethod
    def user(cls, content: str) -> "ChatMessage":
        return cls(role=Role.USER, content=content)

    @classmethod
    def assistant(cls, content: str) -> "ChatMessage":
        return cls(role=Role.ASSISTANT, content=content)

# core/models/chat_message.py