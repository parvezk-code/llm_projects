# core/models/chat_message.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatMessage:
    """
    A single message in the conversation history.
    Passive domain model — immutable, no logic.

    role: "user" | "assistant"
    content: the message text
    """
    role: str
    content: str