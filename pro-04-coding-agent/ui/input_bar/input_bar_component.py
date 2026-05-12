from PyQt6.QtWidgets import QWidget, QHBoxLayout
from ui.input_bar.widgets.text_input_widget import TextInputWidget
from ui.input_bar.widgets.send_button_widget import SendButtonWidget


class InputBarComponent(QWidget):
    """Text input field + Send button."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("inputBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 12)
        layout.setSpacing(8)

        self.text_input = TextInputWidget()
        self.send_button = SendButtonWidget()

        layout.addWidget(self.text_input, stretch=1)
        layout.addWidget(self.send_button)
