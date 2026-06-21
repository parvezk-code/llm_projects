# desktop/state_controller/state_controller.py

from core.models.chat_message import ChatMessage
from core.models.pdf_document import PDFDocument

from desktop.state.app_state import AppState


class StateController:
    """
    The single access point to application state.

    Actions read and update state only through this object. It owns the one
    state object (injected by the Main Controller) and operates directly on
    its data fields. It holds no business or workflow logic and never touches
    UI, Core logic, Gateways, or Event Handlers.
    """

    def __init__(self, app_state: AppState):
        self._state = app_state

    # --- Document ---

    def set_document(self, document: PDFDocument):
        self._state.document = document

    def get_document(self) -> PDFDocument | None:
        return self._state.document

    def has_document(self) -> bool:
        return self._state.document is not None

    def clear_document(self):
        self._state.document = None

    # --- Chat messages ---

    def add_chat_message(self, message: ChatMessage):
        self._state.messages.append(message)

    def get_chat_messages(self) -> list[ChatMessage]:
        return list(self._state.messages)   # copy: callers cannot mutate internal state

    def remove_last_chat_message(self):
        if self._state.messages:
            self._state.messages.pop()

    def is_chat_empty(self) -> bool:
        return not self._state.messages

    def clear_chat(self):
        self._state.messages.clear()

    # --- Processing flag ---

    def set_processing(self, value: bool):
        self._state.is_processing = value

    def is_processing(self) -> bool:
        return self._state.is_processing

# desktop/state_controller/state_controller.py