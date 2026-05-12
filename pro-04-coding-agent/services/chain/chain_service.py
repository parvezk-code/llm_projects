import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage
from conf.settings.openai_config import OpenAIConfig

logger = logging.getLogger(__name__)


class ChainService:
    """
    Owns and runs the LCEL chain:

        prompt | llm | output_parser

    This is the core LangChain Level 1 concept file.

    LCEL concepts introduced here:
    ─────────────────────────────────────────────────────────
    ChatOpenAI          — LangChain wrapper around OpenAI API
    ChatPromptTemplate  — defines system message + history + user turn
    MessagesPlaceholder — injects the full message history into the prompt
    StrOutputParser     — extracts plain string from the LLM response
    LCEL | operator     — chains prompt → llm → parser into a Runnable
    ─────────────────────────────────────────────────────────

    ChainService works with simple types only.
    It receives a system_prompt string, a list of LangChain BaseMessages
    (already converted by ChainController), and a user_input string.
    It returns a plain string answer.
    """

    def __init__(self, config: OpenAIConfig) -> None:
        # ── 1. LLM ──────────────────────────────────────────────────────────
        # ChatOpenAI is LangChain's wrapper for OpenAI chat models.
        # It handles API key auth, model selection, and response parsing.
        self._llm = ChatOpenAI(
            api_key=config.openai_api_key,
            model=config.openai_model,
            # temperature=config.temperature,
            # max_tokens=config.max_tokens,
        )

        # ── 2. Output Parser ─────────────────────────────────────────────────
        # StrOutputParser extracts the plain text string from the LLM's
        # AIMessage response object. Without this, .invoke() returns an
        # AIMessage; with it, we get a clean str.
        self._output_parser = StrOutputParser()

        # ── 3. Prompt Template ───────────────────────────────────────────────
        # ChatPromptTemplate defines the shape of every prompt sent to the LLM.
        #
        # ("system", "{system_prompt}")
        #   → filled with the agent's persona text at runtime
        #
        # MessagesPlaceholder("history")
        #   → filled with the list of HumanMessage/AIMessage history objects
        #     This is how LangChain injects multi-turn conversation context.
        #
        # ("human", "{user_input}")
        #   → filled with the user's current message
        self._prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            MessagesPlaceholder("history"),
            ("human", "{user_input}"),
        ])

        # ── 4. LCEL Chain ────────────────────────────────────────────────────
        # The | operator is LCEL (LangChain Expression Language).
        # It composes Runnables left-to-right:
        #   prompt.invoke(vars) → formatted ChatPromptValue
        #   llm.invoke(...)     → AIMessage
        #   parser.invoke(...)  → str
        #
        # chain.invoke(vars) runs all three steps in sequence.
        self._chain = self._prompt | self._llm | self._output_parser

    def run(
        self,
        system_prompt: str,
        history: list[BaseMessage],
        user_input: str,
    ) -> str:
        """
        Invoke the LCEL chain with the given inputs.

        Parameters
        ----------
        system_prompt : str
            The agent's persona and instructions.
        history : list[BaseMessage]
            Conversation history as LangChain message objects.
            Already converted by ChainController from ChatMessage dataclasses.
        user_input : str
            The user's latest message.

        Returns
        -------
        str
            The assistant's plain text reply.
        """
        logger.debug("ChainService.run — model=%s input_len=%d", self._llm.model_name, len(user_input))

        result: str = self._chain.invoke({
            "system_prompt": system_prompt,
            "history": history,
            "user_input": user_input,
        })

        logger.debug("ChainService.run — response_len=%d", len(result))
        return result
