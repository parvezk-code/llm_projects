# desktop/event_handlers/status_bar_event_handler.py


class StatusBarEventHandler:
    """
    Handles events emitted by the status bar (dismiss).

    The status bar controller is injected, never imported.
    """

    def __init__(self, status_bar_controller):   # StatusBarController
        self._status_bar = status_bar_controller

    def on_dismissed(self):
        self._status_bar.hide_error()

# desktop/event_handlers/status_bar_event_handler.py