# ui/chat_area/widgets/placeholder_widget.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class PlaceholderWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        self._icon_label = QLabel("📄")
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._icon_label.setStyleSheet("font-size: 48px;")

        self._hint_label = QLabel("Upload a PDF to start chatting")
        self._hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hint_label.setStyleSheet("font-size: 14px; color: #888888;")

    def _create_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._icon_label)
        layout.addWidget(self._hint_label)
        self.setLayout(layout)