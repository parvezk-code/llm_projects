# services/service_bundle.py

from dataclasses import dataclass
from services.chain.chain_controller import ChainController
from services.retriever.pipeline.controller import RetrieverPipelineController


@dataclass(frozen=True)
class ServiceBundle:
    chain_controller: ChainController
    retriever_controller: RetrieverPipelineController