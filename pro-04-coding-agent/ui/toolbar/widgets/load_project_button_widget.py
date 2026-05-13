# ui/toolbar/widgets/load_project_button_widget.py

from PyQt6.QtWidgets import QPushButton


class LoadProjectButtonWidget(QPushButton):

    def __init__(self) -> None:
        super().__init__("Load Project")
        self.setObjectName("loadProjectButton")