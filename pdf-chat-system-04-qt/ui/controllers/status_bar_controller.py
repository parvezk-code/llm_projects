# ui/controllers/status_bar_controller.py

from ui.components.status_bar.status_bar_component import StatusBarComponent


class StatusBarController:
    """Owns the UI-level behavior of the error status bar."""

    def __init__(self, component: StatusBarComponent):
        self._component = component

    # --- Signal binding ---

    def bind_dismissed(self, handler):
        self._component.dismissed.connect(handler)

    # --- Operations (one job each) ---

    def show_error(self, message: str):
        self._component.show_error(message)

    def hide_error(self):
        self._component.hide_error()

# ui/controllers/status_bar_controller.py
