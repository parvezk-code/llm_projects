# core_services/vector_stores/faiss/service.py

import logging
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class FAISSVectorStoreService:

    def __init__(self, embeddings: OpenAIEmbeddings) -> None:
        self._embeddings = embeddings

    def build_retriever(self, chunks: list[Document]) -> VectorStoreRetriever:
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self._embeddings,
        )
        retriever = vector_store.as_retriever()
        logger.info(f"FAISS vector store built with {len(chunks)} chunks")
        return retriever