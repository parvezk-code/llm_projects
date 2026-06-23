# ui/chat_area/chat_area_component.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

from ui.chat_area.widgets.placeholder_widget import PlaceholderWidget


class ChatAreaComponent(QWidget):
    """
    Scrollable chat area containing message bubbles.
    Shows PlaceholderWidget when empty.
    No signals — purely a display component.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("chatArea")
        self._create_widgets()
        self._create_layout()
        self._connect_child_signals()

    def _create_widgets(self) -> None:
        self._placeholder = PlaceholderWidget()

        self._container = QWidget()
        self._container.setObjectName("chatContainer")
        self._container_layout = QVBoxLayout(self._container)
        self._container_layout.setContentsMargins(0, 8, 0, 8)
        self._container_layout.setSpacing(2)
        self._container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setObjectName("chatScroll")
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setWidget(self._container)

    def _create_layout(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._placeholder)
        layout.addWidget(self._scroll_area)
        self.setLayout(layout)
        self._scroll_area.hide()

    def _connect_child_signals(self) -> None:
        pass

    # --- Accessors for ChatAreaController ---

    def get_container_layout(self) -> QVBoxLayout:
        return self._container_layout

    def get_scroll_bar(self):
        return self._scroll_area.verticalScrollBar()

    def show_scroll_area(self) -> None:
        self._placeholder.hide()
        self._scroll_area.show()

    def show_placeholder(self) -> None:
        self._scroll_area.hide()
        self._placeholder.show()

# ui/chat_area/chat_area_component.py