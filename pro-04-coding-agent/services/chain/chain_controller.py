# services/chain/chain_controller.py

import logging
from langchain_core.messages import BaseMessage
from services.chain.chain_service import ChainService
from services.chain.request import ChainRequest
from services.chain.response import ChainResponse
from conf.settings.openai_config import OpenAIConfig

logger = logging.getLogger(__name__)


class ChainController:
    """
    Receives a ChainRequest (Pydantic), calls ChainService,
    and returns a ChainResponse (Pydantic).

    History is expected to already be in LangChain BaseMessage format —
    conversion from internal ChatMessage types is the caller's responsibility
    and happens in the transformer layer before the request is built.

    Owns the config dependency — reads api_key and model from OpenAIConfig
    and passes them as plain values to ChainService, keeping ChainService
    portable and free of any app or config coupling.
    """

    def __init__(self, config: OpenAIConfig) -> None:
        self._service = ChainService(
            api_key=config.openai_api_key,
            model=config.openai_model,
        )

    def run(self, request: ChainRequest) -> ChainResponse:
        """
        Call service with already-converted history and return response.

        Steps:
        1. Call ChainService.run() with history as list[BaseMessage]
        2. Wrap result in ChainResponse
        """
        try:
            answer = self._service.run(
                system_prompt=request.system_prompt,
                history=request.history,
                user_input=request.user_input,
            )
            return ChainResponse(answer=answer)

        except Exception as exc:
            logger.exception("ChainController.run failed")
            return ChainResponse(error=str(exc))