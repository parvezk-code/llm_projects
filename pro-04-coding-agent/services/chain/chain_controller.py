# services/chain/chain_controller.py

import logging
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.tools import BaseTool

from services.chain.plain.plain_chain_service import PlainChainService
from services.chain.retrieval.retrieval_chain_service import RetrievalChainService
from services.chain.agent.agent_chain_service import AgentChainService
from services.chain.request import ChainRequest
from services.chain.response import ChainResponse

logger = logging.getLogger(__name__)


class ChainController:

    def __init__(
        self,
        plain_chain_service: PlainChainService,
        retrieval_chain_service: RetrievalChainService,
        agent_chain_service: AgentChainService,
    ) -> None:
        self._plain = plain_chain_service
        self._retrieval = retrieval_chain_service
        self._agent = agent_chain_service

    def run(self, request: ChainRequest) -> ChainResponse:
        try:
            if request.mode == "Agent":
                answer = self._agent.run(
                    history=request.history,
                    user_input=request.user_input,
                )
            elif request.mode == "RAG" and request.retriever is not None:
                answer = self._retrieval.run(
                    history=request.history,
                    user_input=request.user_input,
                    retriever=request.retriever,
                )
            else:
                answer = self._plain.run(
                    history=request.history,
                    user_input=request.user_input,
                )
            return ChainResponse(answer=answer)
        except Exception as e:
            logger.error(f"ChainController error: {e}")
            return ChainResponse(error=str(e))