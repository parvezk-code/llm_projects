# services/chain/retrieval/retrieval_chain_service.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever


class RetrievalChainService:

    def __init__(
        self,
        llm: ChatOpenAI,
        system_prompt: str,
    ) -> None:
        self._llm = llm
        self._system_prompt = system_prompt
        self._output_parser = StrOutputParser()

    def run(
        self,
        history: list,
        user_input: str,
        retriever: VectorStoreRetriever,
    ) -> str:
        system_message = ("system", self._system_prompt + "\n\nContext:\n{context}")
        history_placeholder = MessagesPlaceholder(variable_name="history")
        human_message = ("human", "{input}")

        messages = [system_message, history_placeholder, human_message]
        prompt = ChatPromptTemplate.from_messages(messages)

        context_fetcher = lambda x: retriever.invoke(x["input"])
        history_passer = lambda x: x["history"]
        input_passer = lambda x: x["input"]

        input_map = {
            "context": context_fetcher,
            "history": history_passer,
            "input": input_passer,
        }

        chain = input_map | prompt | self._llm | self._output_parser

        return chain.invoke({
            "history": history,
            "input": user_input,
        })