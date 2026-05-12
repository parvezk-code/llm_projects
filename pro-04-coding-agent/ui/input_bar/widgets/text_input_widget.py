from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent


class TextInputWidget(QTextEdit):
    """
    Multi-line text input.
    Emits submit_triggered on Ctrl+Enter (or Cmd+Enter on macOS).
    Regular Enter adds a newline as normal.
    """

    submit_triggered = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("textInput")
        self.setPlaceholderText("Ask me to write, review, or fix Python code…  (Ctrl+Enter to send)")
        self.setFixedHeight(80)
        self.setEnabled(True)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        is_ctrl = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        is_enter = event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)

        if is_ctrl and is_enter:
            self.submit_triggered.emit()
        else:
            super().keyPressEvent(event)
