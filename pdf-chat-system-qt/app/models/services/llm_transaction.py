# app/models/services/llm_transaction.py

from dataclasses import dataclass, field
from app.models.services.chat_message import ChatMessage


@dataclass
class LLMTransaction:
    pdf_text: str
    history: list[ChatMessage]
    user_message: ChatMessage
    response: ChatMessage = None