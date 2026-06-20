# ui/components/file_picker/file_picker.py

from PyQt6.QtWidgets import QFileDialog, QWidget
from PyQt6.QtCore import pyqtSignal


class FilePickerComponent(QWidget):
    """
    Non-visual component. Launches the native file dialog and reports the
    result through signals. It is created by the page but not laid out.
    """

    pdf_selected = pyqtSignal(str)    # emits selected file path
    dialog_canceled = pyqtSignal()    # emitted when the dialog is dismissed

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

# ui/components/file_picker/file_picker.py
