# app/models/services/llm_transaction/chat_message.py

from dataclasses import dataclass


@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str