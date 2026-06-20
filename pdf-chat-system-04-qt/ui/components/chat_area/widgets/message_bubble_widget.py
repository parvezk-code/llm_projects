# ui/components/chat_area/widgets/message_bubble_widget.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


class MessageBubbleWidget(QWidget):
    """A single chat bubble. Dumb renderer; styled by role via objectName."""

    def __init__(self, role: str, content: str, parent=None):
        super().__init__(parent)
        self._role = role
        self._content = content
        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        self._bubble_label = QLabel(self._content)
        self._bubble_label.setWordWrap(True)
        self._bubble_label.setMaximumWidth(450)
        self._apply_role_object_name()

    def _apply_role_object_name(self):
        if self._role == "user":
            self._bubble_label.setObjectName("userBubble")
        elif self._role == "assistant":
            self._bubble_label.setObjectName("assistantBubble")
        elif self._role == "error":
            self._bubble_label.setObjectName("errorBubble")

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        if self._role == "user":
            layout.addStretch()
            layout.addWidget(self._bubble_label)
        else:
            layout.addWidget(self._bubble_label)
            layout.addStretch()
        self.setLayout(layout)

    # --- Public accessors ---

    def get_role(self) -> str:
        return self._role

    def get_content(self) -> str:
        return self._content

    def update_content(self, content: str):
        self._content = content
        self._bubble_label.setText(content)

# ui/components/chat_area/widgets/message_bubble_widget.py
