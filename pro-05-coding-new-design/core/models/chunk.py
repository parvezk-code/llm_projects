# core/models/chunk.py

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    """
    A single chunk of a document, the unit that gets embedded and retrieved.
    Passive, immutable domain data.

    source_path: which document this chunk came from (for citation/context).
    content:     the chunk text.
    """
    source_path: str
    content: str

    @classmethod
    def create(cls, source_path: str, content: str) -> Chunk:
        return cls(source_path=source_path, content=content)

# core/models/chunk.py