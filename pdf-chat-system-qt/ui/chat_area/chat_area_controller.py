# ui/chat_area/chat_area_controller.py

from PyQt6.QtCore import QTimer
from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.chat_area.widgets.message_bubble_widget import MessageBubbleWidget
from app.models.services.chat_message import ChatMessage


class ChatAreaController:

    def __init__(self, component: ChatAreaComponent):
        self._component = component

    # --- Called by MainController ---

    def emptyAllChats(self):
        self._clear_bubbles()
        self._component.get_placeholder().setVisible(True)

    def waitForLLMCall(self):
        self._component.get_loading_bubble().setVisible(True)
        self._scroll_to_bottom()

    def handleNewMessage(self, usrMessage: ChatMessage, llmMessage: ChatMessage):
        self._component.get_loading_bubble().setVisible(False)
        self._add_message_bubble(usrMessage)
        self._add_message_bubble(llmMessage)

    def handleFailedLLMCall(self, message: str):
        self._component.get_loading_bubble().setVisible(False)
        bubble = MessageBubbleWidget(role="error", content=message)
        layout = self._component.get_scroll_layout()
        loading_bubble = self._component.get_loading_bubble()
        index = layout.indexOf(loading_bubble)
        layout.insertWidget(index, bubble)
        self._scroll_to_bottom()

    # --- Internal ---

    def _add_message_bubble(self, message: ChatMessage):
        bubble = MessageBubbleWidget(
            role=message.role,
            content=message.content
        )
        layout = self._component.get_scroll_layout()
        # Insert before loading bubble (always last)
        loading_bubble = self._component.get_loading_bubble()
        index = layout.indexOf(loading_bubble)
        layout.insertWidget(index, bubble)
        self._scroll_to_bottom()

    def _clear_bubbles(self):
        layout = self._component.get_scroll_layout()
        # Remove all MessageBubbleWidgets, keep placeholder and loading bubble
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, MessageBubbleWidget):
                layout.removeWidget(widget)
                widget.deleteLater()

    def _scroll_to_bottom(self):
        scroll_area = self._component.get_scroll_area()
        scroll_bar = scroll_area.verticalScrollBar()

        def on_range_changed(min, max):
            scroll_bar.setValue(max)
            scroll_bar.rangeChanged.disconnect(on_range_changed)

        scroll_bar.rangeChanged.connect(on_range_changed)