# ui/input_bar/input_bar_component.py

from PyQt6.QtWidgets import QLineEdit


class MessageInputWidget(QLineEdit):
    """Self-contained input field. Owns its own styling and state."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()

    def _setup(self):
        self.setPlaceholderText("Ask a question...")
        self.setFixedHeight(36)
        self.setEnabled(False)
        self.setObjectName("messageInput")

    def get_text(self) -> str:
        return self.text().strip()