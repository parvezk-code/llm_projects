from dataclasses import dataclass


@dataclass
class ChatMessage:
    """
    A single message in the conversation history.
    Internal model — plain dataclass, not Pydantic.

    role: "user" | "assistant"
    content: the message text
    """
    role: str
    content: str
