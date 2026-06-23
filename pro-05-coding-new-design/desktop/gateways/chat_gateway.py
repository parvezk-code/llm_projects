# desktop/gateways/chat_gateway.py

from langchain_core.messages import BaseMessage
from core.services.chat.plain_chat_service import PlainChatService
from core.models.chat_message import ChatMessage

class ChatGateway:
    """
    Bridges Actions to the PlainChatService in Core.
    Accepts history as internal ChatMessage list, converts to LangChain
    types here so Core stays independent of transport concerns.
    Returns a plain string answer.
    """

    def __init__(self, plain_chat_service: PlainChatService) -> None:
        self._service = plain_chat_service

    def send(self, history: list[ChatMessage], user_input: str) -> str:
        lc_history = self._to_langchain_messages(history)
        return self._service.run(history=lc_history, user_input=user_input)

    def _to_langchain_messages(self, history: list[ChatMessage]) -> list[BaseMessage]:
        from langchain_core.messages import HumanMessage, AIMessage
        result: list[BaseMessage] = []
        for msg in history:
            if msg.role == "user":
                result.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                result.append(AIMessage(content=msg.content))
            # unknown roles are silently skipped
        return result