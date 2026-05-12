from PyQt6.QtWidgets import QPushButton


class SendButtonWidget(QPushButton):
    """Send message button."""

    def __init__(self, parent=None) -> None:
        super().__init__("Send", parent)
        self.setObjectName("sendButton")
        self.setEnabled(False)
