# services/chain/plain/plain_chain_service.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


class PlainChainService:

    def __init__(
        self,
        llm: ChatOpenAI,
        system_prompt: str,
    ) -> None:
        self._llm = llm
        self._system_prompt = system_prompt
        self._output_parser = StrOutputParser()

    def run(self, history: list, user_input: str) -> str:
        system_message = ("system", self._system_prompt)
        history_placeholder = MessagesPlaceholder(variable_name="history")
        human_message = ("human", "{user_input}")

        messages = [system_message, history_placeholder, human_message]
        prompt = ChatPromptTemplate.from_messages(messages)

        chain = prompt | self._llm | self._output_parser

        return chain.invoke({
            "history": history,
            "user_input": user_input,
        })