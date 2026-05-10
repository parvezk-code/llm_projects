# services/pdf/pdf_service.py

import fitz  # PyMuPDF


class PDFService:

    def extract_text(self, file_path: str) -> tuple[str, int]:
        with fitz.open(file_path) as doc:
            page_count = len(doc)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
        return full_text, page_count