# app/models/services/pdf_document.py

from dataclasses import dataclass


@dataclass
class PDFDocument:
    filename: str
    full_text: str
    page_count: int