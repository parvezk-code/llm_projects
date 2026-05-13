# core_services/document_extractors/text/plain/service.py

import logging
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class PlainTextExtractorService:

    def extract(self, directory_path: str, allowed_extensions: list[str]) -> list[Document]:
        directory = Path(directory_path)
        documents = []

        for file_path in directory.rglob("*"):
            if file_path.suffix not in allowed_extensions:
                continue
            if not file_path.is_file():
                continue
            try:
                loader = TextLoader(str(file_path), encoding="utf-8")
                docs = loader.load()
                documents.extend(docs)
                logger.debug(f"Loaded: {file_path}")
            except Exception as e:
                logger.warning(f"Skipped {file_path}: {e}")

        logger.info(f"Extracted {len(documents)} documents from {directory_path}")
        return documents