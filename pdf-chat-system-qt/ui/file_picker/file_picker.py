# ui/file_picker/file_picker.py

from PyQt6.QtWidgets import QFileDialog, QWidget
from PyQt6.QtCore import pyqtSignal


class FilePickerComponent(QWidget):

    pdf_selected = pyqtSignal(str)   # emits selected file path
    dialog_canceled = pyqtSignal()   # optional (good practice)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

    def open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF File",
            "",
            "PDF Files (*.pdf)"
        )

        if file_path:
            self.pdf_selected.emit(file_path)
        else:
            self.dialog_canceled.emit()