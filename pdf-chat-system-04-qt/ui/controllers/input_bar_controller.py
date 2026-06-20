# ui/controllers/input_bar_controller.py

from ui.components.input_bar.input_bar_component import InputBarComponent


class InputBarController:
    """Owns the UI-level behavior of the input bar."""

    def __init__(self, component: InputBarComponent):
        self._component = component

    # --- Signal binding ---

    def bind_send_clicked(self, handler):
        self._component.send_clicked.connect(handler)

    # --- Operations (one job each) ---

    def enable_input(self):
        self._component.set_enabled(True)

    def disable_input(self):
        self._component.set_enabled(False)

    def clear_input(self):
        self._component.clear_input()

# ui/controllers/input_bar_controller.py
