# ui/controllers/input_bar_controller.py

from PyQt6.QtCore import QObject

from ui.input_bar.input_bar_component import InputBarComponent


class InputBarController(QObject):
    """
    Manages InputBarComponent.
    Exposes bind methods for external signal wiring and operation methods.
    """

    def __init__(self, component: InputBarComponent) -> None:
        super().__init__()
        self._component = component

    # --- bind methods ---

    def bind_send_triggered(self, method) -> None:
        self._component.send_triggered.connect(method)

    # --- operation methods ---

    def get_text(self) -> str:
        return self._component.get_text()

    def clear_text(self) -> None:
        self._component.clear_text()

    def set_enabled(self, enabled: bool) -> None:
        self._component.set_enabled(enabled)

    # --- event methods (one per event) ---

    def reset_on_clear_chat(self) -> None:
        self.set_enabled(True)

    def reset_on_send_cleared(self) -> None:
        self.clear_text()

# ui/controllers/input_bar_controller.py