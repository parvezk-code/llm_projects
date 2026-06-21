# ui/components/status_bar/status_bar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal


class StatusBarComponent(QWidget):
    """
    Inline error banner. Hidden until an error is shown.

    Styling is controlled entirely by the active QSS theme via the selectors
    StatusBarComponent, StatusBarComponent QLabel, and
    StatusBarComponent QPushButton. No inline styles here.
    """

    dismissed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()
        self._connect_signals()
        self.setVisible(False)

    def _create_widgets(self):
        self._warning_icon = QLabel("⚠")

        self._error_message_label = QLabel("")
        self._error_message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self._dismiss_btn = QPushButton("×")
        self._dismiss_btn.setFixedSize(24, 24)

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(self._warning_icon)
        layout.addWidget(self._error_message_label, stretch=1)
        layout.addWidget(self._dismiss_btn)
        self.setLayout(layout)

    def _connect_signals(self):
        self._dismiss_btn.clicked.connect(self.dismissed)

    # --- Public operations (called by StatusBarController) ---

    def show_error(self, message: str):
        self._error_message_label.setText(message)
        self.setVisible(True)

    def hide_error(self):
        self._error_message_label.setText("")
        self.setVisible(False)

# ui/components/status_bar/status_bar_component.py