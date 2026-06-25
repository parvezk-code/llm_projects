# desktop/gateways/index_gateway.py

from core.models.chunk import Chunk
from core.models.project_index import ProjectIndex
from core.services.extraction.document_extractor_service import DocumentExtractorService
from core.services.chunking.code_chunker_service import CodeChunkerService
from core.services.vector_store.faiss_vector_store_service import FaissVectorStoreService


class IndexGateway:
    """
    Bridges Actions to the RAG indexing pipeline in Core:
        extraction → chunking → embedding → vector store.

    Exposes only what Actions need:
      - build_index(project_path) -> ProjectIndex
      - retrieve(question, index) -> list[Chunk]

    Contains no business logic — orchestrates Core services and adapts results
    into domain models (ProjectIndex, Chunk).
    """

    def __init__(
        self,
        extractor: DocumentExtractorService,
        chunker: CodeChunkerService,
        vector_store: FaissVectorStoreService,
    ) -> None:
        self._extractor = extractor
        self._chunker = chunker
        self._vector_store = vector_store

    def build_index(self, project_path: str) -> ProjectIndex:
        documents = self._extractor.extract(project_path)
        chunks = self._chunker.chunk(documents)
        store = self._vector_store.build(chunks)
        return ProjectIndex.create(
            project_path=project_path,
            store=store,
            chunk_count=len(chunks),
        )

    def retrieve(self, question: str, index: ProjectIndex, top_k: int = 4) -> list[Chunk]:
        return self._vector_store.search(index.store, question, top_k=top_k)

# desktop/gateways/index_gateway.py