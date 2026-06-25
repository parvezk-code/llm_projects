# desktop/gateways/agent_gateway.py

from langchain_core.messages import BaseMessage
from core.services.chat.agent_chat_service import AgentChatService


class AgentGateway:
    """
    Bridges Actions to the AgentChatService in Core.
    Receives pre-shaped LangChain message history (built by the Action) plus the
    user input and project path. Returns the agent's final reply as a string.
    Contains no business logic — delegates only.
    """

    def __init__(self, agent_chat_service: AgentChatService) -> None:
        self._service = agent_chat_service

    def get_agent_reply(
        self,
        history: list[BaseMessage],
        user_input: str,
        project_path: str | None,
    ) -> str:
        return self._service.run(
            history=history,
            user_input=user_input,
            project_path=project_path,
        )

# desktop/gateways/agent_gateway.py