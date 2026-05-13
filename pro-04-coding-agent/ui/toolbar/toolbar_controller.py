# ui/toolbar/toolbar_controller.py

from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QObject, pyqtSignal

from ui.toolbar.toolbar_component import ToolbarComponent


class ToolbarController(QObject):
    """
    Manages toolbar component.
    Owns folder picker dialog logic.
    Exposes bind methods for external signal wiring.
    """

    project_loaded = pyqtSignal(str)

    def __init__(self, component: ToolbarComponent) -> None:
        super().__init__()
        self._component = component
        self._component.load_project_clicked.connect(self._on_load_project_clicked)

    def _on_load_project_clicked(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(
            self._component,
            "Select Project Folder",
        )
        if folder_path:
            self._component.set_project_name(folder_path.split("/")[-1])
            self.project_loaded.emit(folder_path)

    # --- bind methods ---

    def bind_clear_clicked(self, method) -> None:
        self._component.clear_clicked.connect(method)

    def bind_project_loaded(self, method) -> None:
        self.project_loaded.connect(method)

    # --- operation methods ---

    def set_enabled(self, enabled: bool) -> None:
        self._component.set_enabled(enabled)

    def clear_project_label(self) -> None:
        self._component.clear_project_name()