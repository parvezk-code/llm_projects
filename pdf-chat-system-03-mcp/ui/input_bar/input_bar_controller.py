# ui/input_bar/input_bar_controller.py

from ui.input_bar.input_bar_component import InputBarComponent


class InputBarController:

    def __init__(self, component: InputBarComponent):
        self._component = component

    # --- Called by MainController ---

    def bind_send_clicked(self, handler):
        self._component.send_clicked.connect(handler)

    def clear_input(self):
        self._component.clear_input()

    def enableInput(self):
        self._component.set_enabled(True)

    def disableInput(self):
        self._component.set_enabled(False)