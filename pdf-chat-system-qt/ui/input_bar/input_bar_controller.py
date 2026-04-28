# ui/input_bar/input_bar_controller.py

from ui.input_bar.input_bar_component import InputBarComponent


class InputBarController:

    def __init__(self, component: InputBarComponent):
        self._component = component

    # --- Called by MainController ---

    def bind_send_clicked(self, handler):
        self._component.send_clicked.connect(handler)

    def get_text(self) -> str:
        return self._component.get_text()

    def clear_input(self):
        self._component.clear_input()

    def set_enabled(self, enabled: bool):
        self._component.set_enabled(enabled)