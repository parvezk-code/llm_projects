# ui/status_bar/status_bar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class StatusBarComponent(QWidget):
    """
    Error/info banner — shown when an error or status message occurs.
    Hidden by default.
    Emits dismiss_clicked signal.
    """

    dismiss_clicked = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statusBar")
        self._create_widgets()
        self._create_layout()
        self._connect_child_signals()
        self.hide()

    def _create_widgets(self) -> None:
        self._message_label = QLabel("")
        self._message_label.setObjectName("statusMessage")
        self._message_label.setWordWrap(True)

        self._dismiss_button = QPushButton("✕")
        self._dismiss_button.setObjectName("statusDismiss")
        self._dismiss_button.setFixedSize(24, 24)

    def _create_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 6, 16, 6)
        layout.addWidget(self._message_label, stretch=1)
        layout.addWidget(self._dismiss_button)
        self.setLayout(layout)

    def _connect_child_signals(self) -> None:
        self._dismiss_button.clicked.connect(self.dismiss_clicked)

    # --- Accessors for StatusBarController ---

    def set_message(self, message: str) -> None:
        self._message_label.setText(message)

    def clear_message(self) -> None:
        self._message_label.setText("")

# ui/status_bar/status_bar_component.py