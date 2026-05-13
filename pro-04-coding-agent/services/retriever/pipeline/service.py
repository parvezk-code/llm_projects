# services/retriever/pipeline/service.py

import logging
from langchain_core.vectorstores import VectorStoreRetriever

from core_services.document_extractors.text.plain.controller import PlainTextExtractorController
from core_services.document_extractors.text.plain.request import PlainTextExtractorRequest
from core_services.chunking.code.controller import CodeChunkingController
from core_services.chunking.code.request import CodeChunkingRequest
from core_services.vector_stores.faiss.controller import FAISSVectorStoreController
from core_services.vector_stores.faiss.request import FAISSVectorStoreRequest

logger = logging.getLogger(__name__)


class RetrieverPipelineService:

    def __init__(
        self,
        extractor_controller: PlainTextExtractorController,
        chunking_controller: CodeChunkingController,
        vector_store_controller: FAISSVectorStoreController,
    ) -> None:
        self._extractor = extractor_controller
        self._chunker = chunking_controller
        self._vector_store = vector_store_controller

    def build(self, project_path: str) -> VectorStoreRetriever:
        logger.info(f"Starting retriever pipeline for: {project_path}")

        extraction_response = self._extractor.run(
            PlainTextExtractorRequest(directory_path=project_path)
        )
        if extraction_response.has_error():
            raise RuntimeError(f"Extraction failed: {extraction_response.error}")
        if not extraction_response.has_documents():
            raise RuntimeError("No documents found in the selected project folder.")

        chunking_response = self._chunker.run(
            CodeChunkingRequest(documents=extraction_response.documents)
        )
        if chunking_response.has_error():
            raise RuntimeError(f"Chunking failed: {chunking_response.error}")
        if not chunking_response.has_chunks():
            raise RuntimeError("No chunks produced from documents.")

        vector_store_response = self._vector_store.run(
            FAISSVectorStoreRequest(chunks=chunking_response.chunks)
        )
        if vector_store_response.has_error():
            raise RuntimeError(f"Vector store failed: {vector_store_response.error}")

        logger.info("Retriever pipeline completed successfully.")
        return vector_store_response.retriever