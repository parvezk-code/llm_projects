from PyQt6.QtWidgets import QPushButton


class ClearButtonWidget(QPushButton):
    """Clear chat history button."""

    def __init__(self, parent=None) -> None:
        super().__init__("Clear", parent)
        self.setObjectName("clearButton")
        self.setEnabled(False)
