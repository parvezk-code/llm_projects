# ui/toolbar/widgets/project_label_widget.py

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class ProjectLabelWidget(QLabel):
    """
    Displays the loaded project folder name.
    Used at Level 2+ (RAG / Agent / Graph modes).
    Hidden at Level 1.
    """

    def __init__(self) -> None:
        super().__init__("")
        self.setObjectName("projectLabel")
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.hide()

    def set_project_name(self, name: str) -> None:
        self.setText(f"Project: {name}")
        self.show()

    def clear_project_name(self) -> None:
        self.setText("")
        self.hide()

# ui/toolbar/widgets/project_label_widget.py