# ui/toolbar/toolbar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from ui.toolbar.widgets.clear_button_widget import ClearButtonWidget
from ui.toolbar.widgets.load_project_button_widget import LoadProjectButtonWidget
from ui.toolbar.widgets.project_label_widget import ProjectLabelWidget


class ToolbarComponent(QWidget):
    """
    Composes all toolbar widgets.
    Single responsibility: wire children together
    and expose clean signals upward.
    """

    clear_clicked = pyqtSignal()
    load_project_clicked = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("toolbar")
        self._create_widgets()
        self._create_layout()
        self._connect_child_signals()

    def _create_widgets(self) -> None:
        self._clear_button = ClearButtonWidget()
        self._load_project_button = LoadProjectButtonWidget()
        self._project_label = ProjectLabelWidget()

    def _create_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        layout.addWidget(self._clear_button)
        layout.addWidget(self._load_project_button)
        layout.addWidget(self._project_label)
        layout.addStretch()
        self.setLayout(layout)

    def _connect_child_signals(self) -> None:
        self._clear_button.clicked.connect(self.clear_clicked)
        self._load_project_button.clicked.connect(self.load_project_clicked)

    # --- Accessors for ToolbarController ---

    def set_project_name(self, name: str) -> None:
        self._project_label.set_project_name(name)

    def clear_project_name(self) -> None:
        self._project_label.clear_project_name()

    def set_enabled(self, enabled: bool) -> None:
        self._clear_button.setEnabled(enabled)
        self._load_project_button.setEnabled(enabled)
    
    def set_clear_enabled(self, enabled: bool) -> None:
        self._clear_button.setEnabled(enabled)