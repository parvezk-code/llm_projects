from PyQt6.QtCore import pyqtSignal, QObject
from ui.input_bar.input_bar_component import InputBarComponent


class InputBarController(QObject):
    """
    Manages input bar state.
    Exposes send_clicked signal wired from both button click and Ctrl+Enter.
    """

    send_clicked = pyqtSignal()

    def __init__(self, component: InputBarComponent) -> None:
        super().__init__()
        self._component = component

        # Wire both send triggers to the same signal
        self._component.send_button.clicked.connect(self.send_clicked)
        self._component.text_input.submit_triggered.connect(self.send_clicked)

        # Enable send button only when there is text
        self._component.text_input.textChanged.connect(self._on_text_changed)

    def get_text(self) -> str:
        return self._component.text_input.toPlainText().strip()

    def clear_text(self) -> None:
        self._component.text_input.clear()

    def set_enabled(self, enabled: bool) -> None:
        self._component.text_input.setEnabled(enabled)
        self._sync_send_button()

    def _on_text_changed(self) -> None:
        self._sync_send_button()

    def _sync_send_button(self) -> None:
        has_text = bool(self._component.text_input.toPlainText().strip())
        is_enabled = self._component.text_input.isEnabled()
        self._component.send_button.setEnabled(has_text and is_enabled)
