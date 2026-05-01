# ui/input_bar/input_bar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from ui.input_bar.widgets.button_widget import SendButtonWidget
from ui.input_bar.widgets.text_input_widget import MessageInputWidget


class InputBarComponent(QWidget):
    """
    Composes MessageInputWidget + SendButtonWidget.
    Single responsibility: wire the two children together
    and expose one clean signal upward.
    """

    send_clicked = pyqtSignal(str)  # the only signal the controller cares about

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()
        self._connect_child_signals()

    def _create_widgets(self):
        self._message_input = MessageInputWidget()
        self._send_btn = SendButtonWidget()

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.addWidget(self._message_input, stretch=1)
        layout.addWidget(self._send_btn)
        self.setLayout(layout)

    def _connect_child_signals(self):
        self._message_input.returnPressed.connect(self._on_send)
        self._send_btn.clicked.connect(self._on_send)

    def _on_send(self):
        """Single handler for both Enter key and button click."""
        text = self._message_input.get_text()
        if text:
            self.send_clicked.emit(text)
            # self._message_input.clear()

    def set_enabled(self, enabled: bool):
        self._message_input.setEnabled(enabled)
        self._send_btn.setEnabled(enabled)
    
    def clear_input(self):
        self._message_input.clear()