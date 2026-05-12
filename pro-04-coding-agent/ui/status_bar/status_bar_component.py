from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class StatusBarComponent(QWidget):
    """
    Error banner — shown at the bottom when an error occurs.
    Hidden by default.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statusBar")
        self.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 6, 16, 6)

        self.message_label = QLabel("")
        self.message_label.setObjectName("statusMessage")
        self.message_label.setWordWrap(True)

        self.dismiss_button = QPushButton("✕")
        self.dismiss_button.setObjectName("statusDismiss")
        self.dismiss_button.setFixedSize(24, 24)

        layout.addWidget(self.message_label, stretch=1)
        layout.addWidget(self.dismiss_button)
