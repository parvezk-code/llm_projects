# ui/chat_area/widgets/loading_bubble_widget.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class LoadingBubbleWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        self._dots_label = QLabel("● ● ●")
        self._dots_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._dots_label.setStyleSheet("""
            background-color: #E8E8E8;
            color: #888888;
            border-radius: 12px;
            padding: 8px 14px;
            font-size: 14px;
        """)

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        layout.addWidget(self._dots_label)
        layout.addStretch()
        self.setLayout(layout)