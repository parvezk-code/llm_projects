# app/models/state/app_state.py

from dataclasses import dataclass, field
from app.models.services.pdf_document import PDFDocument
from app.models.services.chat_message import ChatMessage


@dataclass
class AppState:
    pdf: PDFDocument | None = None
    messages: list[ChatMessage] = field(default_factory=list)
    is_loading: bool = False
    error: str | None = None