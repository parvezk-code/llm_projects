# core/services/chunking/code_chunker_service.py

from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.models.document import Document
from core.models.chunk import Chunk


class CodeChunkerService:
    """
    Splits documents into chunks using LangChain's language-aware
    RecursiveCharacterTextSplitter (Python grammar). Splitting on natural code
    boundaries (functions, classes, blank lines) yields far fewer, more coherent
    chunks than blind fixed-window slicing — which keeps embedding fast.

    The Python splitter degrades gracefully on non-Python text (.txt/.js/.java):
    it simply falls back to generic separators. One splitter covers all text
    types, matching the original fast behaviour.

    Returns passive Chunk models.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self._splitter = RecursiveCharacterTextSplitter.from_language(
            language="python",
            chunk_size=chunk_size,
            chunk_overlap=overlap,
        )

    def chunk(self, documents: list[Document]) -> list[Chunk]:
        chunks: list[Chunk] = []
        for document in documents:
            for piece in self._splitter.split_text(document.content):
                chunks.append(Chunk.create(source_path=document.path, content=piece))
        return chunks

# core/services/chunking/code_chunker_service.py