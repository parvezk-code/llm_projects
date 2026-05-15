# services/chain/agent/agent_chain_service.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent


class AgentChainService:

    def __init__(
        self,
        llm: ChatOpenAI,
        system_prompt: str,
        tools: list[BaseTool],
    ) -> None:
        self._system_prompt = system_prompt
        self._tools = tools
        self._agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=system_prompt,
        )

    def run(self, history: list, user_input: str) -> str:
        messages = list(history) + [HumanMessage(content=user_input)]
        result = self._agent.invoke({"messages": messages})
        return result["messages"][-1].content