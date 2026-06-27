# ui/controllers/toolbar_controller.py

from PyQt6.QtCore import QObject

from ui.toolbar.toolbar_component import ToolbarComponent


class ToolbarController(QObject):
    """
    Manages ToolbarComponent.
    Exposes bind methods for external signal wiring and operation methods.
    """

    def __init__(self, component: ToolbarComponent) -> None:
        super().__init__()
        self._component = component
        self._project_loaded = False

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

    def set_load_project_enabled(self, enabled: bool) -> None:
        """Enable Load Project button at Level 2+."""
        self._component.set_load_project_enabled(enabled)

    def set_project_name(self, name: str) -> None:
        self._component.set_project_name(name)
        self._project_loaded = True

    def clear_project_label(self) -> None:
        self._component.clear_project_name()
        self._project_loaded = False

    def has_project_loaded(self) -> bool:
        """UI-level flag: whether a project label is currently shown."""
        return self._project_loaded

    def get_mode(self) -> str:
        return self._component.get_mode()

    def unlock_level(self, level: int) -> None:
        """Unlock UI controls for the given level (called by MainController at startup)."""
        self._component.unlock_level(level)

    # --- event methods (one per event; compose the operations above) ---

    def reset_on_clear_chat(self) -> None:
        self.set_clear_enabled(False)
        self.clear_project_label()

    def reset_on_project_loaded(self, name: str) -> None:
        self.set_project_name(name)
        self.set_clear_enabled(True)

# ui/controllers/toolbar_controller.py