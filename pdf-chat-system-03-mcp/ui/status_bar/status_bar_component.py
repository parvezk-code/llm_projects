# ui/status_bar/status_bar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal


class StatusBarComponent(QWidget):

    dismissed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()
        self._connect_internal_signals()
        self.setVisible(False)

    def _create_widgets(self):
        self._warning_icon = QLabel("⚠")
        self._warning_icon.setStyleSheet("font-size: 14px; color: #CC0000;")

        self._error_message_label = QLabel("")
        self._error_message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._error_message_label.setStyleSheet(
            "font-size: 13px; color: #CC0000;")

        self._dismiss_btn = QPushButton("×")
        self._dismiss_btn.setFixedSize(24, 24)
        self._dismiss_btn.setStyleSheet("""
            QPushButton {
                border: none;
                color: #CC0000;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #990000;
            }
        """)

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(self._warning_icon)
        layout.addWidget(self._error_message_label, stretch=1)
        layout.addWidget(self._dismiss_btn)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #FFDEDE;")

    def _connect_internal_signals(self):
        self._dismiss_btn.clicked.connect(self.dismissed)

    # --- Accessors for StatusBarController ---

    def show_error(self, message: str):
        self._error_message_label.setText(message)
        self.setVisible(True)

    def hide_error(self):
        self._error_message_label.setText("")
        self.setVisible(False)