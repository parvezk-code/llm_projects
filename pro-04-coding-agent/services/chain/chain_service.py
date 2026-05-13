# services/chain/chain_service.py

import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever

logger = logging.getLogger(__name__)


class ChainService:

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: int,
        system_prompt: str,
    ) -> None:
        self._system_prompt = system_prompt
        self._llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self._output_parser = StrOutputParser()

    def run(
        self,
        history: list,
        user_input: str,
        retriever: VectorStoreRetriever | None = None,
    ) -> str:
        if retriever is not None:
            return self._run_retrieval_chain(
                history=history,
                user_input=user_input,
                retriever=retriever,
            )
        return self._run_plain_chain(
            history=history,
            user_input=user_input,
        )

    def _run_plain_chain(self, history: list, user_input: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}"),
        ])
        chain = prompt | self._llm | self._output_parser
        result = chain.invoke({
            "history": history,
            "user_input": user_input,
        })
        logger.info("Plain chain completed.")
        return result

    def _run_retrieval_chain(
        self,
        history: list,
        user_input: str,
        retriever: VectorStoreRetriever,
    ) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._system_prompt + "\n\nContext:\n{context}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        chain = (
            {
                "context": lambda x: retriever.invoke(x["input"]),
                "history": lambda x: x["history"],
                "input": lambda x: x["input"],
            }
            | prompt
            | self._llm
            | self._output_parser
        )
        result = chain.invoke({
            "history": history,
            "input": user_input,
        })
        logger.info("Retrieval chain completed.")
        return result