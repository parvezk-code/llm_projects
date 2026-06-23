# core/services/chat/plain_chat_service.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class PlainChatService:
    """
    Wraps the OpenAI LangChain client.
    Accepts a pre-shaped provider message list (list[dict] with 'role'/'content')
    built by the Action — this service knows nothing about ChatMessage or history shaping.
    Returns the assistant reply as a plain string.
    """

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int) -> None:
        self._llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def get_reply(self, messages: list[dict]) -> str:
        """
        messages: list of dicts with 'role' ('system'|'user'|'assistant') and 'content'.
        Returns the assistant reply text.
        """
        lc_messages = []
        for m in messages:
            role = m["role"]
            content = m["content"]
            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
        return self._llm.invoke(lc_messages).content

# core/services/chat/plain_chat_service.py