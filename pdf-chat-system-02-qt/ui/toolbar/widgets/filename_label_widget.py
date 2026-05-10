# ui/toolbar/widgets/filename_label_widget.py

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class FilenameLabelWidget(QLabel):
    """Displays the loaded PDF filename. Owns its own styling and state."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()

    def _setup(self):
        self.setText("No PDF loaded")
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setObjectName("filenameLabel")

    def set_filename(self, filename: str):
        self.setText(f"📄 {filename}")

    def set_no_pdf(self):
        self.setText("No PDF loaded")