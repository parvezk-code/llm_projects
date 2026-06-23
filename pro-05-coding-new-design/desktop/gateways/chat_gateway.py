# desktop/gateways/chat_gateway.py

from core.services.chat.plain_chat_service import PlainChatService


class ChatGateway:
    """
    Bridges Actions to PlainChatService in Core.
    Accepts a pre-shaped provider message list (built by the Action).
    Returns the assistant reply as a plain string.
    Contains no business logic — delegates and returns.
    """

    def __init__(self, plain_chat_service: PlainChatService) -> None:
        self._service = plain_chat_service

    def get_reply(self, messages: list[dict]) -> str:
        return self._service.get_reply(messages)

# desktop/gateways/chat_gateway.py