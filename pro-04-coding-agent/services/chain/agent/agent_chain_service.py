# services/chain/agent/agent_chain_service.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent


class AgentChainService:

    def __init__(
        self,
        llm: ChatOpenAI,
        system_prompt: str,
        tools: list[BaseTool],
    ) -> None:
        self._llm = llm
        self._base_system_prompt = system_prompt
        self._tools = tools

    def run(
        self,
        history: list,
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