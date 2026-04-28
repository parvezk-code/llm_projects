# ui/chat_area/chat_area_component.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea)
from PyQt6.QtCore import Qt
from ui.chat_area.widgets.placeholder_widget import PlaceholderWidget
from ui.chat_area.widgets.message_bubble_widget import MessageBubbleWidget
from ui.chat_area.widgets.loading_bubble_widget import LoadingBubbleWidget


class ChatAreaComponent(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        # Scroll area
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setStyleSheet("border: none;")

        # Scroll content container
        self._scroll_content = QWidget()
        self._scroll_layout = QVBoxLayout(self._scroll_content)
        self._scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scroll_layout.setSpacing(4)
        self._scroll_layout.setContentsMargins(8, 8, 8, 8)

        # Dumb child widgets
        self._placeholder = PlaceholderWidget()
        self._loading_bubble = LoadingBubbleWidget()
        self._loading_bubble.setVisible(False)

        # Add placeholder to scroll layout
        self._scroll_layout.addWidget(self._placeholder)
        self._scroll_layout.addWidget(self._loading_bubble)

        self._scroll_area.setWidget(self._scroll_content)

    def _create_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._scroll_area)
        self.setLayout(layout)

    # --- Accessors for ChatAreaController ---

    def get_scroll_area(self) -> QScrollArea:
        return self._scroll_area

    def get_scroll_layout(self) -> QVBoxLayout:
        return self._scroll_layout

    def get_placeholder(self) -> PlaceholderWidget:
        return self._placeholder

    def get_loading_bubble(self) -> LoadingBubbleWidget:
        return self._loading_bubble