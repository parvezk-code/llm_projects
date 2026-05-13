# services/chain/chain_service.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever


class ChainService:
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int, system_prompt: str) -> None:    
        self._system_prompt = system_prompt
        self._llm = ChatOpenAI(api_key=api_key, model=model, temperature=temperature, max_tokens=max_tokens) 
        self._output_parser = StrOutputParser()

    # ── Runners ───────────────────────────────────────────────────────────────

    def run_plain_chain(self, history: list, user_input: str) -> str:
        chain = self.get_plain_chain()
        return chain.invoke({"history": history, "user_input": user_input})

    def run_retrieval_chain(self, history: list, user_input: str, retriever: VectorStoreRetriever) -> str:
        chain = self.get_retrieval_chain(retriever)
        return chain.invoke({"history": history, "input": user_input})

    # ── Prompt builders ───────────────────────────────────────────────────────

    def get_plain_prompt(self) -> ChatPromptTemplate:
        system_message          =   ("system", self._system_prompt)
        history_placeholder     =   MessagesPlaceholder(variable_name="history")
        human_message           =   ("human", "{user_input}")
        messages                =   [system_message, history_placeholder, human_message]

        return ChatPromptTemplate.from_messages(messages)

    def get_retrieval_prompt(self) -> ChatPromptTemplate:
        system_message          =   ("system", self._system_prompt + "\n\nContext:\n{context}")
        history_placeholder     =   MessagesPlaceholder(variable_name="history")
        human_message           =   ("human", "{input}")
        messages                =   [system_message, history_placeholder, human_message]

        return ChatPromptTemplate.from_messages(messages)

    # ── Chain builders ────────────────────────────────────────────────────────

    def get_plain_chain(self):
        return self.get_plain_prompt() | self._llm | self._output_parser

    def get_retrieval_chain(self, retriever: VectorStoreRetriever):
        fetcher         =   lambda x: retriever.invoke(x["input"])
        history         =   lambda x: x["history"]
        input_parser    =   lambda x: x["input"]
        input_map       =   { "context": fetcher,  "history": history, "input": input_parser }
        chain           =   ( input_map | self.get_retrieval_prompt() | self._llm  | self._output_parser)

        return chain