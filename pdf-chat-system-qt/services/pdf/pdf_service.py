# services/pdf/pdf_service.py

import fitz  # PyMuPDF


class PDFService:

    def extract_text(self, file_path: str) -> tuple[str, int]:
        doc = fitz.open(file_path)
        page_count = len(doc)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text, page_count