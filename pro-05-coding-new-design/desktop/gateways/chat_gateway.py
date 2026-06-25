# desktop/gateways/chat_gateway.py

from core.services.chat.plain_chat_service import PlainChatService
from core.services.chat.retrieval_chat_service import RetrievalChatService


class ChatGateway:
    """
    Bridges Actions to the chat services in Core.
    Accepts pre-shaped provider message lists (built by the Action).
    Returns the assistant reply as a plain string.
    Contains no business logic — delegates only.

    Level 2: gains get_rag_reply for the retrieval generation path.
    """

    def __init__(
        self,
        plain_chat_service: PlainChatService,
        retrieval_chat_service: RetrievalChatService,
    ) -> None:
        self._plain = plain_chat_service
        self._retrieval = retrieval_chat_service

    def get_reply(self, messages: list[dict]) -> str:
        return self._plain.get_reply(messages)

    def get_rag_reply(self, messages: list[dict]) -> str:
        return self._retrieval.get_reply(messages)

# desktop/gateways/chat_gateway.py