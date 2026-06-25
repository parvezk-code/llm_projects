# desktop/event_handlers/status_bar/dismiss_handler.py

from ui.controllers.status_bar_controller import StatusBarController


class DismissHandler:
    """
    Handles StatusBarComponent.dismiss_clicked.
    Single responsibility: hide the status-bar banner.
    """

    def __init__(self, status_bar: StatusBarController) -> None:
        self._status_bar = status_bar

    def on_dismissed(self) -> None:
        self._status_bar.hide()

# desktop/event_handlers/status_bar/dismiss_handler.py