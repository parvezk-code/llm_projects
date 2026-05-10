# app/models/services/llm_transaction/tool_rounds.py

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel


# ─────────────────────────────────────────────
# ToolCall — pure data, no LLM knowledge
# ─────────────────────────────────────────────

@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


# ─────────────────────────────────────────────
# ToolResult base — Pydantic for model_dump()
# ─────────────────────────────────────────────

class ToolResult(BaseModel):
    tool_call_id: str
    name: str
    arguments: dict[str, Any]
    success: bool
    error_message: str | None = None


# ─────────────────────────────────────────────
# Tool-specific ToolResult subclasses
# ─────────────────────────────────────────────

class GetWorkingDirectoryToolResult(ToolResult):
    name: str = "get_working_directory"
    arguments: dict[str, Any] = {}
    directory_path: str | None = None


class ListPDFsToolResult(ToolResult):
    name: str = "list_pdfs_in_directory"
    directory_path: str | None = None
    pdf_files: list[str] | None = None
    total_count: int | None = None


class ReadPDFContentToolResult(ToolResult):
    name: str = "read_pdf_content"
    pdf_path: str | None = None
    full_text: str | None = None
    page_count: int | None = None


# ─────────────────────────────────────────────
# ToolRound — pure container, no LLM knowledge
# ─────────────────────────────────────────────

@dataclass
class ToolRound:
    round_no: int
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_results: list[ToolResult] = field(default_factory=list)