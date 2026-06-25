# core/models/project_index.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProjectIndex:
    """
    An immutable handle to a built vector index for one loaded project.

    Wraps the third-party vector store (e.g. a FAISS store / retriever) as an
    opaque object so that State and Actions stay independent of the provider.
    The provider specifics live inside Core's vector_store service; everything
    above treats this as a passive domain model.

    project_path: the folder this index was built from (shown in the UI).
    store:        opaque vector-store handle (FAISS, etc.) — never inspected
                  outside Core's vector_store service.
    chunk_count:  how many chunks were indexed (informational).
    """
    project_path: str
    store: Any
    chunk_count: int

    @classmethod
    def create(cls, project_path: str, store: Any, chunk_count: int) -> ProjectIndex:
        return cls(project_path=project_path, store=store, chunk_count=chunk_count)

# core/models/project_index.py