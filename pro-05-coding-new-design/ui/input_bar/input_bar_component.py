# ui/input_bar/input_bar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from ui.input_bar.widgets.text_input_widget import TextInputWidget
from ui.input_bar.widgets.send_button_widget import SendButtonWidget


class InputBarComponent(QWidget):
    """
    Text input field + Send button.
    Emits send_triggered signal on button click or Ctrl+Enter.
    """

    send_triggered = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("inputBar")
        self._create_widgets()
        self._create_layout()
        self._connect_child_signals()

    def _create_widgets(self) -> None:
        self._text_input = TextInputWidget()
        self._send_button = SendButtonWidget()

    def _create_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 8, 12, 12)
        layout.setSpacing(8)
        layout.addWidget(self._text_input, stretch=1)
        layout.addWidget(self._send_button)
        self.setLayout(layout)

    def _connect_child_signals(self) -> None:
        self._send_button.clicked.connect(self.send_triggered)
        self._text_input.submit_triggered.connect(self.send_triggered)
        self._text_input.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self) -> None:
        has_text = bool(self._text_input.toPlainText().strip())
        is_enabled = self._text_input.isEnabled()
        self._send_button.setEnabled(has_text and is_enabled)

    # --- Accessors for InputBarController ---

    def get_text(self) -> str:
        return self._text_input.toPlainText().strip()

    def clear_text(self) -> None:
        self._text_input.clear()

    def set_enabled(self, enabled: bool) -> None:
        self._text_input.setEnabled(enabled)
        has_text = bool(self._text_input.toPlainText().strip())
        self._send_button.setEnabled(enabled and has_text)

# ui/input_bar/input_bar_component.py