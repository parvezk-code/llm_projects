# app/event_handlers/pdf/upload_pdf_handler.py

import os
from app.models.state.app_state import AppState
from app.models.services.pdf_document import PDFDocument
from services.document_extractors.pdf.pymupdf.request import PyMuPDFRequest
from ui.ui_bundle import UIBundle
from services.service_bundle import ServiceBundle


class UploadPDFHandler:

    def __init__(self, state: AppState, ui: UIBundle, svc: ServiceBundle):
        self._state = state
        self._ui = ui
        self._svc = svc

    def on_upload_clicked(self):
        self._ui.file_picker.open_pdf()

    def on_pdf_selected(self, file_path: str):
        request = PyMuPDFRequest(file_path=file_path)
        response = self._svc.pdf.extract(request)

        if response.has_error():
            self._on_load_failed(response.error)
            return

        pdf = PDFDocument(
            filename=os.path.basename(file_path),
            full_text=response.full_text,
            page_count=response.page_count
        )

        self._state.pdf = pdf
        # self._state.messages = []
        # self._state.error = None
        self._ui.toolbar.on_pdf_loaded(pdf)
        # self._ui.status_bar.hide_error()
        # self._ui.chat_area.emptyAllChats()
        # self._ui.input_bar.enableInput()

    def _on_load_failed(self, message: str):
        self._state.error = message
        self._ui.status_bar.show_error(message)