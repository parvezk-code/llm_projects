# ui/toolbar/toolbar_controller.py

from PyQt6.QtWidgets import QFileDialog
from ui.toolbar.toolbar_component import ToolbarComponent
from app.models.services.pdf_document import PDFDocument


class ToolbarController:

    def __init__(self, component: ToolbarComponent):
        self._component = component

    # --- Called by MainController ---

    def bind_upload_requested(self, handler):
        self._component.upload_clicked.connect(handler)

    def bind_clear_clicked(self, handler):
        self._component.clear_clicked.connect(handler)

    def open_file_picker(self) -> str | None:
        file_path, _ = QFileDialog.getOpenFileName(
            self._component,
            "Open PDF File",
            "",
            "PDF Files (*.pdf)"
        )
        return file_path if file_path else None

    def show_pdf(self, pdf: PDFDocument):
        self._component.set_filename(pdf.filename)
        self._component.set_clear_enabled(True)

    def show_no_pdf(self):
        self._component.set_no_pdf()
        self._component.set_clear_enabled(False)