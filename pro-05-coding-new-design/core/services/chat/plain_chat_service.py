# core/services/chat/plain_chat_service.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage


class PlainChatService:
    """
    Owns the plain LCEL chain: prompt | llm | output_parser.
    Wraps LangChain specifics so nothing outside core imports them.
    Accepts pre-converted LangChain message history from the caller.
    """

    def __init__(self, llm: ChatOpenAI, system_prompt: str) -> None:
        self._llm = llm
        self._system_prompt = system_prompt
        self._output_parser = StrOutputParser()

    def run(self, history: list[BaseMessage], user_input: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
        ])
        chain = prompt | self._llm | self._output_parser
        return chain.invoke({
            "history": history,
            "user_input": user_input,
        })