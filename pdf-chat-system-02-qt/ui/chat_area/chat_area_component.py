# ui/chat_area/chat_area_component.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from ui.chat_area.widgets.placeholder_widget import PlaceholderWidget
from ui.chat_area.widgets.message_bubble_widget import MessageBubbleWidget


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
        self._scroll_layout.addWidget(self._placeholder)

        self._scroll_area.setWidget(self._scroll_content)

    def _create_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._scroll_area)
        self.setLayout(layout)

    # --- Called by ChatAreaController ---

    def add_message(self, role: str, content: str):
        bubble = MessageBubbleWidget(role=role, content=content)
        self._scroll_layout.addWidget(bubble)
        self._scroll_to_bottom()

    def show_error(self, message: str):
        bubble = MessageBubbleWidget(role="error", content=message)
        self._scroll_layout.addWidget(bubble)
        self._scroll_to_bottom()

    def clear_messages(self):
        for i in reversed(range(self._scroll_layout.count())):
            widget = self._scroll_layout.itemAt(i).widget()
            if isinstance(widget, MessageBubbleWidget):
                self._scroll_layout.removeWidget(widget)
                widget.deleteLater()
        self._placeholder.setVisible(True)

    # --- Internal ---

    def _scroll_to_bottom(self):
        scroll_bar = self._scroll_area.verticalScrollBar()

        def on_range_changed(min, max):
            scroll_bar.setValue(max)
            scroll_bar.rangeChanged.disconnect(on_range_changed)

        scroll_bar.rangeChanged.connect(on_range_changed)
