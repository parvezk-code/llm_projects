# ui/toolbar/toolbar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal


class ToolbarComponent(QWidget):

    upload_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()
        self._connect_internal_signals()

    def _create_widgets(self):
        self._upload_btn = QPushButton("Upload PDF")
        self._upload_btn.setFixedHeight(32)

        self._filename_label = QLabel("No PDF loaded")
        self._filename_label.setAlignment(Qt.AlignmentFlag.AlignLeft |
                                          Qt.AlignmentFlag.AlignVCenter)
        self._filename_label.setStyleSheet("color: #555555; font-size: 13px;")

        self._clear_btn = QPushButton("Clear")
        self._clear_btn.setFixedHeight(32)
        self._clear_btn.setEnabled(False)

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.addWidget(self._upload_btn)
        layout.addWidget(self._filename_label, stretch=1)
        layout.addWidget(self._clear_btn)
        self.setLayout(layout)

    def _connect_internal_signals(self):
        self._upload_btn.clicked.connect(self.upload_clicked)
        self._clear_btn.clicked.connect(self.clear_clicked)

    # --- Accessors for ToolbarController ---

    def set_filename(self, filename: str):
        self._filename_label.setText(f"📄 {filename}")

    def set_no_pdf(self):
        self._filename_label.setText("No PDF loaded")

    def set_clear_enabled(self, enabled: bool):
        self._clear_btn.setEnabled(enabled)