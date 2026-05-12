# app/transformers/chain/history_transformer.py

import logging
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from app.state.models.chat_message import ChatMessage

logger = logging.getLogger(__name__)


def convert_history(history: list[ChatMessage]) -> list[BaseMessage]:
    """
    Convert internal ChatMessage dataclasses to LangChain BaseMessage types.

    ChatMessage(role="user", ...)      → HumanMessage(content=...)
    ChatMessage(role="assistant", ...) → AIMessage(content=...)

    LangChain requires its own message types so it can serialise them
    correctly into the prompt template via MessagesPlaceholder.
    Unknown roles are skipped with a warning.
    """
    messages: list[BaseMessage] = []
    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))
        else:
            logger.warning("convert_history: unknown role '%s' — skipping", msg.role)
    return messages