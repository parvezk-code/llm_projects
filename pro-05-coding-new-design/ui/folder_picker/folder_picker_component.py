# ui/folder_picker/folder_picker_component.py

from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtCore import pyqtSignal


class FolderPickerComponent(QWidget):
    """
    Wraps QFileDialog for folder selection.
    Emits folder_selected signal when a folder is chosen.
    Emits nothing if user cancels.
    Used at Level 2+ (RAG / Agent / Graph modes).
    """

    folder_selected = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()
        self._connect_child_signals()

    def _create_widgets(self) -> None:
        self._dialog = QFileDialog(self)
        self._dialog.setFileMode(QFileDialog.FileMode.Directory)
        self._dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

    def _create_layout(self) -> None:
        pass

    def _connect_child_signals(self) -> None:
        self._dialog.fileSelected.connect(self.folder_selected)

    # --- Accessors for FolderPickerController ---

    def open(self) -> None:
        self._dialog.open()

# ui/folder_picker/folder_picker_component.py