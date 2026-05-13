# ui/toolbar/toolbar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from ui.toolbar.widgets.clear_button_widget import ClearButtonWidget
from ui.toolbar.widgets.load_project_button_widget import LoadProjectButtonWidget
from ui.toolbar.widgets.project_label_widget import ProjectLabelWidget


class ToolbarComponent(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("toolbar")

        self.clear_button = ClearButtonWidget()
        self.load_project_button = LoadProjectButtonWidget()
        self.project_label = ProjectLabelWidget()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.load_project_button)
        layout.addWidget(self.project_label)
        layout.addStretch()