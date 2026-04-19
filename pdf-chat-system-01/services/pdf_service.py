from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from pypdf import PdfReader


@dataclass
class ExtractedDoc:
    text: str
    page_count: int
    used_ocr: bool


class PDFService:
    """
    Wraps PDF extraction logic.
    Raises RuntimeError (propagated from _extract()) on failure.
    """

    _MIN_CHARS_PER_PAGE = 10

    def extract(self, pdf_bytes: bytes) -> ExtractedDoc:
        """Extract text from raw PDF bytes. Raises RuntimeError on failure."""
        reader = PdfReader(BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        pages_text = [(page.extract_text() or "") for page in reader.pages]
        text = "\n\n".join(pages_text).strip()

        if page_count > 0 and len(text) >= page_count * self._MIN_CHARS_PER_PAGE:
            return ExtractedDoc(text=text, page_count=page_count, used_ocr=False)

        ocr_text = self._ocr_extract(pdf_bytes)
        return ExtractedDoc(text=ocr_text, page_count=page_count, used_ocr=True)

    def _ocr_extract(self, pdf_bytes: bytes) -> str:
        try:
            from pdf2image import convert_from_bytes
            import pytesseract
        except ImportError as e:
            raise RuntimeError(
                "OCR fallback needs `pdf2image` and `pytesseract`. "
                "Install with `pip install pdf2image pytesseract`."
            ) from e

        try:
            images = convert_from_bytes(pdf_bytes)
        except Exception as e:
            raise RuntimeError(
                "OCR fallback failed while rasterizing the PDF. "
                "On macOS: `brew install poppler`."
            ) from e

        pages: list[str] = []
        for img in images:
            try:
                pages.append(pytesseract.image_to_string(img))
            except pytesseract.TesseractNotFoundError as e:
                raise RuntimeError(
                    "Tesseract binary not found. On macOS: `brew install tesseract`."
                ) from e

        return "\n\n".join(pages).strip()
