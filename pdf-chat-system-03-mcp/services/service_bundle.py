# services/service_bundle.py

from dataclasses import dataclass                                        # fix typo
from services.document_extractors.pdf.pymupdf.controller import PyMuPDFController
from services.llm.llm_controller import LLMController
from services.mcp.executor.controller import MCPToolController


@dataclass(frozen=True)
class ServiceBundle:
    pdf: PyMuPDFController
    llm: LLMController
    mcp: MCPToolController