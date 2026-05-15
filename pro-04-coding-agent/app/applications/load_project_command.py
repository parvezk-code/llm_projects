# app/applications/load_project_command.py

from app.state.state_controller import StateController
from services.document_extractors.text.plain.request import PlainTextExtractorRequest
from services.document_extractors.text.plain.response import PlainTextExtractorResponse
from services.chunking.code.request import CodeChunkingRequest
from services.vector_stores.faiss.request import FAISSVectorStoreRequest
from services.service_bundle import ServiceBundle


class LoadProjectCommand:

    def __init__(
        self,
        state: StateController,
        service: ServiceBundle,
    ) -> None:
        self._state = state
        self._service = service

    def execute(self, project_path: str):
        extraction_response = self._service.extractor_controller.run(
            PlainTextExtractorRequest(directory_path=project_path)
        )
        if extraction_response.has_error():
            return extraction_response
        if not extraction_response.has_documents():
            extraction_response.error = "No documents found in selected folder."
            return extraction_response

        chunking_response = self._service.chunking_controller.run(
            CodeChunkingRequest(documents=extraction_response.documents)
        )
        if chunking_response.has_error():
            return chunking_response
        if not chunking_response.has_chunks():
            chunking_response.error = "No chunks produced from documents."
            return chunking_response

        vector_store_response = self._service.vector_store_controller.run(
            FAISSVectorStoreRequest(chunks=chunking_response.chunks)
        )
        if not vector_store_response.has_error():
            self._state.set_project_path(project_path)

        return vector_store_response