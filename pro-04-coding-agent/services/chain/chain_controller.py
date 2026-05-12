import logging
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from services.chain.chain_service import ChainService
from services.chain.request import ChainRequest
from services.chain.response import ChainResponse

logger = logging.getLogger(__name__)


class ChainController:
    """
    Receives a ChainRequest (Pydantic), converts internal ChatMessage
    dataclasses into LangChain message types, calls ChainService,
    and returns a ChainResponse (Pydantic).

    This is the boundary between the app's internal world (dataclasses)
    and LangChain's world (BaseMessage subclasses).

    LangChain concepts introduced here:
    ────────────────────────────────────────────────────────
    HumanMessage  — LangChain type for a user turn in history
    AIMessage     — LangChain type for an assistant turn in history
    ────────────────────────────────────────────────────────
    """

    def __init__(self, chain_service: ChainService) -> None:
        self._service = chain_service

    def run(self, request: ChainRequest) -> ChainResponse:
        """
        Convert history → call service → return response.

        Steps:
        1. Convert list[ChatMessage] to list[BaseMessage] (LangChain types)
        2. Call ChainService.run()
        3. Wrap result in ChainResponse
        """
        try:
            lc_history = self._convert_history(request.history)

            answer = self._service.run(
                system_prompt=request.system_prompt,
                history=lc_history,
                user_input=request.user_input,
            )

            return ChainResponse(answer=answer)

        except Exception as exc:
            logger.exception("ChainController.run failed")
            return ChainResponse(error=str(exc))

    def _convert_history(self, history) -> list[BaseMessage]:
        """
        Convert internal ChatMessage dataclasses to LangChain BaseMessage types.

        ChatMessage(role="user", ...)      → HumanMessage(content=...)
        ChatMessage(role="assistant", ...) → AIMessage(content=...)

        LangChain requires its own message types so it can serialise them
        correctly into the prompt template via MessagesPlaceholder.
        """
        messages: list[BaseMessage] = []
        for msg in history:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(AIMessage(content=msg.content))
            else:
                logger.warning("Unknown role '%s' — skipping", msg.role)
        return messages
