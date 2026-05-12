from PyQt6.QtCore import QTimer
from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.chat_area.widgets.message_bubble_widget import MessageBubbleWidget


class ChatAreaController:
    """
    Manages chat bubbles, scroll position, and placeholder visibility.
    """

    def __init__(self, component: ChatAreaComponent) -> None:
        self._component = component

    def add_bubble(self, role: str, content: str) -> None:
        """Append a message bubble and scroll to bottom."""
        bubble = MessageBubbleWidget(role, content)
        self._component.container_layout.addWidget(bubble)
        self._show_chat()
        QTimer.singleShot(50, self._scroll_to_bottom)

    def clear(self) -> None:
        """Remove all bubbles and show placeholder."""
        layout = self._component.container_layout
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._show_placeholder()

    def _scroll_to_bottom(self) -> None:
        bar = self._component.scroll_area.verticalScrollBar()
        bar.setValue(bar.maximum())

    def _show_chat(self) -> None:
        self._component.placeholder.hide()
        self._component.scroll_area.show()

    def _show_placeholder(self) -> None:
        self._component.scroll_area.hide()
        self._component.placeholder.show()
