# ui/status_bar/status_bar_controller.py

from ui.status_bar.status_bar_component import StatusBarComponent


class StatusBarController:
    """
    Manages status bar component.
    Exposes bind methods for external signal wiring.
    """

    def __init__(self, component: StatusBarComponent) -> None:
        self._component = component
        self._component.dismiss_clicked.connect(self.hide)

    # --- bind methods ---

    def bind_dismiss_clicked(self, method) -> None:
        self._component.dismiss_clicked.connect(method)

    # --- operation methods ---

    def show_error(self, message: str) -> None:
        self._component.set_message(f"⚠  {message}")
        self._component.show()

    def hide(self) -> None:
        self._component.hide()
        self._component.clear_message()