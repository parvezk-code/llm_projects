# core/models/pdf_document.py

from dataclasses import dataclass


@dataclass(frozen=True)
class PDFDocument:
    """A loaded PDF and its extracted text."""

    filename: str      # display name, e.g. "report.pdf"
    file_path: str     # absolute path on disk
    text: str          # full extracted text (used as LLM context)
    page_count: int

# core/models/pdf_document.py