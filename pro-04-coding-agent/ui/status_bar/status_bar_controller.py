from ui.status_bar.status_bar_component import StatusBarComponent


class StatusBarController:
    """Show or hide the error banner."""

    def __init__(self, component: StatusBarComponent) -> None:
        self._component = component
        self._component.dismiss_button.clicked.connect(self.hide)

    def show_error(self, message: str) -> None:
        self._component.message_label.setText(f"⚠  {message}")
        self._component.show()

    def hide(self) -> None:
        self._component.hide()
        self._component.message_label.setText("")
