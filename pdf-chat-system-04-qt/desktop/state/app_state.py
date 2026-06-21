# desktop/state/app_state.py

from core.models.chat_message import ChatMessage
from core.models.pdf_document import PDFDocument


class AppState:
    """
    The single application state object. Holds DATA ONLY — no methods, no
    logic. Every read and write happens in the StateController. State never
    touches UI, Core logic, Gateways, or Actions.
    """

    def __init__(self):
        self.document: PDFDocument | None = None
        self.messages: list[ChatMessage] = []
        self.is_processing: bool = False

# desktop/state/app_state.py