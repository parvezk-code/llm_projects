# ui/chat_area/widgets/message_bubble_widget.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class MessageBubbleWidget(QWidget):

    def __init__(self, role: str, content: str, parent=None):
        super().__init__(parent)
        self._role = role
        self._content = content
        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        self._bubble_label = QLabel(self._content)
        self._bubble_label.setWordWrap(True)
        self._bubble_label.setMaximumWidth(450)

        if self._role == "user":
            self._bubble_label.setStyleSheet("""
                background-color: #DCF8C6;
                color: #000000;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 14px;
            """)
        elif self._role == "assistant":
            self._bubble_label.setStyleSheet("""
                background-color: #E8E8E8;
                color: #000000;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 14px;
            """)
        elif self._role == "error":
            self._bubble_label.setStyleSheet("""
                background-color: #FFDEDE;
                color: #CC0000;
                border-radius: 12px;
                padding: 8px 14px;
                font-size: 14px;
            """)

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)

        if self._role == "user":
            layout.addStretch()
            layout.addWidget(self._bubble_label)
        else:
            layout.addWidget(self._bubble_label)
            layout.addStretch()

        self.setLayout(layout)