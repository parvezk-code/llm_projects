# core/services/extraction/document_extractor_service.py

import os
from core.models.document import Document


class DocumentExtractorService:
    """
    Walks a project folder and extracts text documents from it.
    Core service — owns the filesystem-walking specifics.
    Returns passive Document models; no chunking, no embedding here.

    Extensions are injected (config-driven) so the indexed file set is tunable
    without code changes. One read path covers all text types — there is no
    per-extension extraction logic, by design.
    """

    DEFAULT_EXTENSIONS = (".py", ".txt", ".js", ".java")
    SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".idea", ".mypy_cache"}

    def __init__(self, extensions: tuple[str, ...] | None = None) -> None:
        self._extensions = tuple(extensions) if extensions else self.DEFAULT_EXTENSIONS

    def extract(self, project_path: str) -> list[Document]:
        documents: list[Document] = []
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            for filename in files:
                if not filename.endswith(self._extensions):
                    continue
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except OSError:
                    continue
                if content.strip():
                    documents.append(Document.create(path=full_path, content=content))
        return documents

# core/services/extraction/document_extractor_service.py