# services/pdf_reader.py

from pathlib import Path
import fitz  # PyMuPDF


class PDFReader:

    def read(self, path: Path) -> tuple[str, int]:
        doc = fitz.open(str(path))

        full_text = ""
        for page in doc:
            full_text += page.get_text()

        return full_text.strip(), len(doc)