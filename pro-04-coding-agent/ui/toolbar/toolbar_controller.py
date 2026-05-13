# ui/toolbar/toolbar_controller.py

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import pyqtSignal, QObject
from ui.toolbar.toolbar_component import ToolbarComponent


class ToolbarController(QObject):
    clear_clicked = pyqtSignal()
    project_loaded = pyqtSignal(str)

    def __init__(self, component: ToolbarComponent) -> None:
        super().__init__()
        self._component = component
        self._bind_signals()

    def _bind_signals(self) -> None:
        self._component.clear_button.clicked.connect(self.clear_clicked.emit)
        self._component.load_project_button.clicked.connect(self._on_load_project_clicked)

    def _on_load_project_clicked(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(
            self._component,
            "Select Project Folder",
        )
        if folder_path:
            self._component.project_label.set_project_name(folder_path.split("/")[-1])
            self.project_loaded.emit(folder_path)

    def set_enabled(self, enabled: bool) -> None:
        self._component.clear_button.setEnabled(enabled)
        self._component.load_project_button.setEnabled(enabled)

    def clear_project_label(self) -> None:
        self._component.project_label.clear_project_name()