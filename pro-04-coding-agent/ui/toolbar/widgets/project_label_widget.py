# ui/toolbar/widgets/project_label_widget.py

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class ProjectLabelWidget(QLabel):

    def __init__(self) -> None:
        super().__init__("No project loaded")
        self.setObjectName("projectLabel")
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

    def set_project_name(self, name: str) -> None:
        self.setText(f"Project: {name}")

    def clear_project_name(self) -> None:
        self.setText("No project loaded")