from PyQt6.QtCore import pyqtSignal, QObject
from ui.toolbar.toolbar_component import ToolbarComponent


class ToolbarController(QObject):
    """
    Controls the toolbar state.
    Exposes clear_clicked signal for MainController to connect to.
    """

    clear_clicked = pyqtSignal()

    def __init__(self, component: ToolbarComponent) -> None:
        super().__init__()
        self._component = component
        self._component.clear_button.clicked.connect(self.clear_clicked)

    def set_clear_enabled(self, enabled: bool) -> None:
        self._component.clear_button.setEnabled(enabled)
