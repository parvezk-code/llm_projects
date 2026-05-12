from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class MessageBubbleWidget(QWidget):
    """
    A single chat message bubble.
    Aligned right for user messages, left for assistant messages.
    """

    def __init__(self, role: str, content: str, parent=None) -> None:
        super().__init__(parent)
        self._role = role

        outer = QHBoxLayout(self)
        outer.setContentsMargins(12, 4, 12, 4)
        outer.setSpacing(0)

        self._label = QLabel(content)
        self._label.setWordWrap(True)
        self._label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self._label.setObjectName(
            "userBubble" if role == "user" else "assistantBubble"
        )

        if role == "user":
            outer.addStretch()
            outer.addWidget(self._label)
        else:
            outer.addWidget(self._label)
            outer.addStretch()
