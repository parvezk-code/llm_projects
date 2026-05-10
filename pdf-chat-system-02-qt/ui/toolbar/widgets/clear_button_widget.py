# ui/toolbar/widgets/clear_button_widget.py

from PyQt6.QtWidgets import QPushButton


class ClearButtonWidget(QPushButton):
    """Clear button. Owns its own styling and state."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()

    def _setup(self):
        self.setText("Clear")
        self.setFixedHeight(32)
        self.setEnabled(False)
        self.setObjectName("clearBtn")
        self.setProperty("state", "default")

    def set_state(self, state: str):
        self.setProperty("state", state)
        self.style().unpolish(self)
        self.style().polish(self)