# desktop/actions/document/upload_document_action.py

from core.models.pdf_document import PDFDocument

from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle


class UploadDocumentAction:
    """
    Workflow: load a PDF from disk and make it the active document.

    Steps: call the PDF gateway (which reaches Core) to build a PDFDocument,
    store it in state, and start a fresh chat for the new document.
    Returns the PDFDocument so the Event Handler can update the UI.
    """

    def __init__(self, state_controller: StateController, gateways: GatewayBundle):
        self._state = state_controller
        self._gateways = gateways

    def execute(self, file_path: str) -> PDFDocument:
        document = self._gateways.pdf.load_document(file_path)   # gateway -> Core
        self._state.set_document(document)                       # write state
        self._state.clear_chat()                                 # fresh chat for new doc
        return document

# desktop/actions/document/upload_document_action.py