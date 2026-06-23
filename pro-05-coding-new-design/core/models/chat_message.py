# core/models/chat_message.py

from __future__ import annotations
from dataclasses import dataclass


class Role:
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class ChatMessage:
    """
    A single message in the conversation history.
    Passive, immutable domain model — no workflow logic, no to_dict().
    ChatMessage → dict conversion belongs in the Action.

    Factory constructors keep call sites clean.
    """
    role: str
    content: str

    @classmethod
    def user(cls, content: str) -> ChatMessage:
        return cls(role=Role.USER, content=content)

    @classmethod
    def assistant(cls, content: str) -> ChatMessage:
        return cls(role=Role.ASSISTANT, content=content)

# core/models/chat_message.py