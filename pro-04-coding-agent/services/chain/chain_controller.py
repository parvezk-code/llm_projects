# services/chain/chain_controller.py

import logging
from services.chain.chain_service import ChainService
from services.chain.request import ChainRequest
from services.chain.response import ChainResponse

logger = logging.getLogger(__name__)


class ChainController:

    def __init__(self, service: ChainService) -> None:
        self._service = service

    def run(self, request: ChainRequest) -> ChainResponse:
        try:
            answer = self._service.run(
                history=request.history,
                user_input=request.user_input,
                retriever=request.retriever,
            )
            return ChainResponse(answer=answer)
        except Exception as e:
            logger.error(f"ChainController error: {e}")
            return ChainResponse(error=str(e))