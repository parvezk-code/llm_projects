# ui/status_bar/status_bar_controller.py

from ui.status_bar.status_bar_component import StatusBarComponent


class StatusBarController:

    def __init__(self, component: StatusBarComponent):
        self._component = component

    # --- Called by MainController ---

    def bind_dismissed(self, handler):
        self._component.dismissed.connect(handler)

    def show_error(self, message: str):
        self._component.show_error(message)

    def hide_error(self):
        self._component.hide_error()