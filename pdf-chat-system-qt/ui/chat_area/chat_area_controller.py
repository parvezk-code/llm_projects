# ui/chat_area/chat_area_controller.py

from ui.chat_area.chat_area_component import ChatAreaComponent
from app.models.services.chat_message import ChatMessage


class ChatAreaController:

    def __init__(self, component: ChatAreaComponent):
        self._component = component

    # --- Called by MainController ---

    def emptyAllChats(self):
        self._component.clear_messages()

    def handleNewMessage(self, usrMessage: ChatMessage, llmMessage: ChatMessage):
        self._component.add_message(usrMessage.role, usrMessage.content)
        self._component.add_message(llmMessage.role, llmMessage.content)

    def handleFailedLLMCall(self, message: str):
        self._component.show_error(message)
