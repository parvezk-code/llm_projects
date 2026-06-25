# core/services/chat/agent_chat_service.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain.agents import create_agent


class AgentChatService:
    """
    Wraps a tool-using agent (LangChain create_agent).
    Core service — owns the agent/provider specifics, builds its own LLM.

    Builds the agent fresh per call with the LLM + tools, augments the system
    prompt with the loaded project path, and returns the final message content.

    Receives history as a pre-built list of LangChain messages (the Action shapes
    internal ChatMessage history into LangChain types before calling, keeping
    transport shaping in the Action).
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
        tools: list[BaseTool],
    ) -> None:
        self._llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self._base_system_prompt = system_prompt
        self._tools = tools

    def run(
        self,
        history: list[BaseMessage],
        user_input: str,
        project_path: str | None = None,
    ) -> str:
        system_prompt = self._build_system_prompt(project_path)

        agent = create_agent(
            model=self._llm,
            tools=self._tools,
            system_prompt=system_prompt,
        )

        messages = list(history) + [HumanMessage(content=user_input)]
        result = agent.invoke({"messages": messages})
        return result["messages"][-1].content

    def _build_system_prompt(self, project_path: str | None) -> str:
        if project_path:
            return (
                self._base_system_prompt
                + f"\n\nThe user has loaded a project at: {project_path}\n"
                + "You can explore it using list_directory and read files using read_file."
            )
        return self._base_system_prompt

# core/services/chat/agent_chat_service.py