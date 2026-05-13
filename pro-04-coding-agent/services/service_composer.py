# services/service_composer.py

from conf.settings.config_bundle import ConfigBundle

from services.document_extractors.text.plain.service import PlainTextExtractorService
from services.document_extractors.text.plain.controller import PlainTextExtractorController
from services.chunking.code.service import CodeChunkingService
from services.chunking.code.controller import CodeChunkingController
from services.embedding_generators.openai.service import OpenAIEmbeddingService
from services.embedding_generators.openai.controller import OpenAIEmbeddingController
from services.vector_stores.faiss.service import FAISSVectorStoreService
from services.vector_stores.faiss.controller import FAISSVectorStoreController
from services.chain.chain_service import ChainService
from services.chain.chain_controller import ChainController
from services.retriever.pipeline.service import RetrieverPipelineService
from services.retriever.pipeline.controller import RetrieverPipelineController
from services.service_bundle import ServiceBundle


class ServiceComposer:

    def __init__(self, config: ConfigBundle) -> None:
        self._config = config

    def compose(self) -> ServiceBundle:

        # --- chain ---
        chain_service = ChainService(
            api_key=self._config.openai.openai_api_key,
            model=self._config.openai.openai_model,
            temperature=self._config.openai.temperature,
            max_tokens=self._config.openai.max_tokens,
            system_prompt=self._config.app.system_prompt,
        )
        chain_controller = ChainController(service=chain_service)

        # --- document extractor ---
        extractor_service = PlainTextExtractorService()
        extractor_controller = PlainTextExtractorController(
            service=extractor_service,
            allowed_extensions=self._config.retriever.allowed_extensions,
        )

        # --- chunking ---
        chunking_service = CodeChunkingService()
        chunking_controller = CodeChunkingController(
            service=chunking_service,
            chunk_size=self._config.retriever.chunk_size,
            chunk_overlap=self._config.retriever.chunk_overlap,
        )

        # --- embeddings ---
        embedding_service = OpenAIEmbeddingService(
            model=self._config.retriever.embedding_model,
            api_key=self._config.openai.openai_api_key,
        )
        embedding_controller = OpenAIEmbeddingController(service=embedding_service)

        # --- vector store ---
        vector_store_service = FAISSVectorStoreService(
            embeddings=embedding_service.get_embeddings_model()
        )
        vector_store_controller = FAISSVectorStoreController(service=vector_store_service)

        # --- retriever pipeline ---
        retriever_pipeline_service = RetrieverPipelineService(
            extractor_controller=extractor_controller,
            chunking_controller=chunking_controller,
            vector_store_controller=vector_store_controller,
        )
        retriever_controller = RetrieverPipelineController(
            service=retriever_pipeline_service
        )

        return ServiceBundle(
            chain_controller=chain_controller,
            retriever_controller=retriever_controller,
            extractor_controller=extractor_controller,
            chunking_controller=chunking_controller,
            embedding_controller=embedding_controller,
            vector_store_controller=vector_store_controller,
        )