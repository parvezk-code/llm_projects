from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ui.toolbar.widgets.clear_button_widget import ClearButtonWidget


class ToolbarComponent(QWidget):
    """
    Top toolbar — app title label + Clear button.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("toolbar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)

        self.title_label = QLabel("Coding Agent")
        self.title_label.setObjectName("toolbarTitle")

        self.clear_button = ClearButtonWidget()

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.clear_button)
