# ui/input_bar/widgets/button_widget.py

from PyQt6.QtWidgets import QPushButton


class SendButtonWidget(QPushButton):
    """Self-contained send button. Owns its own styling and state."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()

    def _setup(self):
        self.setText("Send")
        self.setFixedSize(72, 36)
        self.setEnabled(False)
        self.setObjectName("sendBtn")