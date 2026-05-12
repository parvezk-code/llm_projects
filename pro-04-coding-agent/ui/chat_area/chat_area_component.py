from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from ui.chat_area.widgets.placeholder_widget import PlaceholderWidget


class ChatAreaComponent(QWidget):
    """
    Scrollable chat area containing message bubbles.
    Shows PlaceholderWidget when empty.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("chatArea")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Scroll area ──────────────────────────────────────────────────────
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("chatScroll")
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Container inside scroll area
        self.container = QWidget()
        self.container.setObjectName("chatContainer")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 8, 0, 8)
        self.container_layout.setSpacing(2)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.container)

        # ── Placeholder ──────────────────────────────────────────────────────
        self.placeholder = PlaceholderWidget()

        root_layout.addWidget(self.placeholder)
        root_layout.addWidget(self.scroll_area)

        self.scroll_area.hide()
