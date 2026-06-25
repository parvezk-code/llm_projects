# core/models/document.py

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    """
    A single extracted source document (e.g. one code/text file from a project).
    Passive, immutable domain data — no logic, no serialisation.
    """
    path: str
    content: str

    @classmethod
    def create(cls, path: str, content: str) -> Document:
        return cls(path=path, content=content)

# core/models/document.py