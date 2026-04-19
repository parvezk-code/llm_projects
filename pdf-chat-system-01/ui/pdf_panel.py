import streamlit as st


class PDFPanelUI:
    """
    Renders PDF-related widgets.
    Completely stateless — receives all display values as arguments,
    returns raw bytes from the uploader for the Controller to process.
    """

    def render_uploader(self, uploader_key: int) -> bytes | None:
        """Render file uploader. Returns raw bytes if a file is present, else None."""
        uploaded = st.file_uploader(
            "Upload a PDF",
            type=["pdf"],
            key=f"uploader_{uploader_key}",
        )
        return uploaded.getvalue() if uploaded is not None else None

    def render_metadata(
        self,
        page_count: int,
        used_ocr: bool,
        char_count: int,
    ) -> None:
        """Display page count, extraction method, and character count."""
        method = "OCR" if used_ocr else "PyPDF"
        st.caption(
            f"{page_count} pages · extracted via {method} · {char_count:,} chars"
        )

    def render_truncation_warning(self) -> None:
        st.warning(
            "PDF exceeds the context budget; later pages were truncated. "
            "v1 has no retrieval — consider a smaller PDF."
        )

    def render_extraction_error(self, message: str) -> None:
        st.error(message)
