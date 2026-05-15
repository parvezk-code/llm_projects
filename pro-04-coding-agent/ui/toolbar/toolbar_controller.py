# ui/toolbar/toolbar_controller.py

from PyQt6.QtCore import QObject

from ui.toolbar.toolbar_component import ToolbarComponent


class ToolbarController(QObject):

    def __init__(self, component: ToolbarComponent) -> None:
        super().__init__()
        self._component = component

    # --- bind methods ---

    def bind_clear_clicked(self, method) -> None:
        self._component.clear_clicked.connect(method)

    def bind_load_project_clicked(self, method) -> None:
        self._component.load_project_clicked.connect(method)

    def bind_mode_changed(self, method) -> None:
        self._component.mode_changed.connect(method)

    # --- operation methods ---

    def set_enabled(self, enabled: bool) -> None:
        self._component.set_enabled(enabled)

    def set_clear_enabled(self, enabled: bool) -> None:
        self._component.set_clear_enabled(enabled)

    def set_project_name(self, name: str) -> None:
        self._component.set_project_name(name)

    def clear_project_label(self) -> None:
        self._component.clear_project_name()

    def get_mode(self) -> str:
        return self._component.get_mode()