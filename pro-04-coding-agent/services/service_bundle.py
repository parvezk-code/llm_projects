# services/service_bundle.py

from dataclasses import dataclass
from services.chain.chain_controller import ChainController
from services.retriever.pipeline.controller import RetrieverPipelineController
from services.document_extractors.text.plain.controller import PlainTextExtractorController
from services.chunking.code.controller import CodeChunkingController
from services.embedding_generators.openai.controller import OpenAIEmbeddingController
from services.vector_stores.faiss.controller import FAISSVectorStoreController


@dataclass(frozen=True)
class ServiceBundle:
    chain_controller: ChainController
    retriever_controller: RetrieverPipelineController
    extractor_controller: PlainTextExtractorController
    chunking_controller: CodeChunkingController
    embedding_controller: OpenAIEmbeddingController
    vector_store_controller: FAISSVectorStoreController