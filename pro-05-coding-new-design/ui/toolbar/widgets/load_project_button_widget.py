# ui/toolbar/widgets/load_project_button_widget.py

from PyQt6.QtWidgets import QPushButton


class LoadProjectButtonWidget(QPushButton):
    """
    Load Project button.
    Used at Level 2+ (RAG / Agent / Graph modes).
    Disabled at Level 1.
    """

    def __init__(self, parent=None) -> None:
        super().__init__("Load Project", parent)
        self.setObjectName("loadProjectButton")
        self.setEnabled(False)

# ui/toolbar/widgets/load_project_button_widget.py