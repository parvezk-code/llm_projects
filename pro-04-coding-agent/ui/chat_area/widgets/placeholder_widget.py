from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class PlaceholderWidget(QWidget):
    """
    Shown in the chat area when there are no messages.
    Displays a prompt icon and hint text.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("placeholder")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon_label = QLabel("⌨")
        icon_label.setObjectName("placeholderIcon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hint_label = QLabel("Ask me to write, review, or fix Python code")
        hint_label.setObjectName("placeholderHint")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_label)
        layout.addWidget(hint_label)
