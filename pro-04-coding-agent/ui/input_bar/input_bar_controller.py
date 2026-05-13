# ui/input_bar/input_bar_controller.py

from PyQt6.QtCore import QObject, pyqtSignal

from ui.input_bar.input_bar_component import InputBarComponent


class InputBarController(QObject):
    """
    Manages input bar component.
    Exposes bind methods for external signal wiring.
    """

    send_clicked = pyqtSignal()

    def __init__(self, component: InputBarComponent) -> None:
        super().__init__()
        self._component = component
        self._component.send_triggered.connect(self.send_clicked)

    # --- bind methods ---

    def bind_send_clicked(self, method) -> None:
        self._component.send_triggered.connect(method)

    # --- operation methods ---

    def get_text(self) -> str:
        return self._component.get_text()

    def clear_text(self) -> None:
        self._component.clear_text()

    def set_enabled(self, enabled: bool) -> None:
        self._component.set_enabled(enabled)