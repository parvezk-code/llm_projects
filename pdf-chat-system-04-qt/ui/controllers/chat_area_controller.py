# ui/controllers/chat_area_controller.py

from ui.components.chat_area.chat_area_component import ChatAreaComponent


class ChatAreaController:
    """
    Owns the UI-level behavior of the chat area. Consumes primitives only;
    Core models (e.g. ChatMessage) are unpacked by the Event Handler before
    these methods are called.
    """

    def __init__(self, component: ChatAreaComponent):
        self._component = component

    # --- Operations (one job each; primitives only) ---

    def add_message(self, role: str, content: str):
        self._component.add_message(role, content)

    def show_error(self, message: str):
        self._component.show_error(message)

    def clear_chat(self):
        self._component.clear_messages()

# ui/controllers/chat_area_controller.py
