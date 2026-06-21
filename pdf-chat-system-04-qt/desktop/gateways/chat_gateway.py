# desktop/gateways/chat_gateway.py

from core.services.llm_service import LLMService


class ChatGateway:
    """
    Stable interface for the chat/LLM operations Actions need.

    In local mode it wraps the Core LLMService directly. In remote mode an
    equivalent gateway would call the API client instead — Actions see the
    same interface either way.

    Messages are passed in the provider-neutral [{"role", "content"}] shape.
    Building that list (ChatMessage -> dict conversion) is the Action's job,
    not the gateway's and not the model's.
    """

    def __init__(self, llm_service: LLMService):
        self._llm_service = llm_service

    def get_reply(self, messages: list[dict]) -> str:
        return self._llm_service.call(messages)

# desktop/gateways/chat_gateway.py