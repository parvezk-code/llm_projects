# core/services/chat/retrieval_chat_service.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class RetrievalChatService:
    """
    RAG generation: answers a question using retrieved context + history.
    Core service — wraps the OpenAI LangChain client.

    Receives an already-assembled provider message list (list[dict]) built by
    the Action. Context-block shaping (chunks → text) is the Action's job, not
    this service's — this service only assembles LangChain messages and calls
    the model.
    """

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int) -> None:
        self._llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def get_reply(self, messages: list[dict]) -> str:
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

# core/services/chat/retrieval_chat_service.py