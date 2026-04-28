# ui/input_bar/input_bar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal


class InputBarComponent(QWidget):

    send_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()
        self._connect_internal_signals()

    def _create_widgets(self):
        self._message_input = QLineEdit()
        self._message_input.setPlaceholderText("Ask a question...")
        self._message_input.setFixedHeight(36)
        self._message_input.setEnabled(False)
        self._message_input.setStyleSheet("font-size: 14px; padding: 4px 8px;")

        self._send_btn = QPushButton("Send")
        self._send_btn.setFixedSize(72, 36)
        self._send_btn.setEnabled(False)
        self._send_btn.setStyleSheet("font-size: 14px;")

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.addWidget(self._message_input, stretch=1)
        layout.addWidget(self._send_btn)
        self.setLayout(layout)

    def _connect_internal_signals(self):
        self._send_btn.clicked.connect(self.send_clicked)
        self._message_input.returnPressed.connect(self.send_clicked)

    # --- Accessors for InputBarController ---

    def get_text(self) -> str:
        return self._message_input.text().strip()

    def clear_input(self):
        self._message_input.clear()

    def set_enabled(self, enabled: bool):
        self._message_input.setEnabled(enabled)
        self._send_btn.setEnabled(enabled)