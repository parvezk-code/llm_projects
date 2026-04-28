# ui/chat_area/chat_area_controller.py

from PyQt6.QtCore import Qt
from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.chat_area.widgets.message_bubble_widget import MessageBubbleWidget
from app.models.services.chat_message import ChatMessage


class ChatAreaController:

    def __init__(self, component: ChatAreaComponent):
        self._component = component

    # --- Called by MainController ---

    def show_placeholder(self):
        self._component.get_placeholder().setVisible(True)

    def hide_placeholder(self):
        self._component.get_placeholder().setVisible(False)

    def show_loading(self):
        self._component.get_loading_bubble().setVisible(True)
        self._scroll_to_bottom()

    def hide_loading(self):
        self._component.get_loading_bubble().setVisible(False)

    def add_message_bubble(self, message: ChatMessage):
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

    def add_error_bubble(self, message: str):
        bubble = MessageBubbleWidget(role="error", content=message)
        layout = self._component.get_scroll_layout()
        loading_bubble = self._component.get_loading_bubble()
        index = layout.indexOf(loading_bubble)
        layout.insertWidget(index, bubble)
        self._scroll_to_bottom()

    def clear_bubbles(self):
        layout = self._component.get_scroll_layout()
        # Remove all MessageBubbleWidgets, keep placeholder and loading bubble
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, MessageBubbleWidget):
                layout.removeWidget(widget)
                widget.deleteLater()

    # --- Internal ---

    def _scroll_to_bottom(self):
        scroll_area = self._component.get_scroll_area()
        scroll_bar = scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())