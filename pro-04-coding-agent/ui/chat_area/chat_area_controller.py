# ui/chat_area/chat_area_controller.py

from PyQt6.QtCore import QTimer

from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.chat_area.widgets.message_bubble_widget import MessageBubbleWidget


class ChatAreaController:
    """
    Manages chat bubbles, scroll position, and placeholder visibility.
    Exposes bind methods for external signal wiring.
    """

    def __init__(self, component: ChatAreaComponent) -> None:
        self._component = component

    # --- bind methods ---

    # no external signals on chat area currently

    # --- operation methods ---

    def add_bubble(self, role: str, content: str) -> None:
        bubble = MessageBubbleWidget(role, content)
        self._component.get_container_layout().addWidget(bubble)
        self._component.show_scroll_area()
        QTimer.singleShot(50, self._scroll_to_bottom)

    def clear_last_bubble(self) -> None:
        layout = self._component.get_container_layout()
        if layout.count():
            item = layout.takeAt(layout.count() - 1)
            if item.widget():
                item.widget().deleteLater()
        if not layout.count():
            self._component.show_placeholder()

    def clear(self) -> None:
        layout = self._component.get_container_layout()
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._component.show_placeholder()

    def _scroll_to_bottom(self) -> None:
        bar = self._component.get_scroll_bar()
        bar.setValue(bar.maximum())