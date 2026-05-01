# ui/toolbar/widgets/upload_button_widget.py

from PyQt6.QtWidgets import QPushButton


class UploadButtonWidget(QPushButton):
    """Upload PDF button. Owns its own styling."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()

    def _setup(self):
        self.setText("Upload PDF")
        self.setFixedHeight(32)
        self.setObjectName("uploadBtn")