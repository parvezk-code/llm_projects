# ui/toolbar/toolbar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from ui.toolbar.widgets.clear_button_widget import ClearButtonWidget
from ui.toolbar.widgets.load_project_button_widget import LoadProjectButtonWidget
from ui.toolbar.widgets.project_label_widget import ProjectLabelWidget
from ui.toolbar.widgets.mode_combo_widget import ModeComboWidget


class ToolbarComponent(QWidget):
    """
    Toolbar containing Clear, Load Project, project label, and mode selector.
    Emits clear_clicked, load_project_clicked, mode_changed signals.
    Load Project and mode selector (RAG/Agent/Graph) are disabled at Level 1.
    """

    clear_clicked = pyqtSignal()
    load_project_clicked = pyqtSignal()
    mode_changed = pyqtSignal(str)

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
        self._mode_combo = ModeComboWidget()
        # Level 1: only Simple mode is selectable
        self._mode_combo.set_level(1)

    def _create_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        layout.addWidget(self._clear_button)
        layout.addWidget(self._load_project_button)
        layout.addWidget(self._project_label)
        layout.addStretch()
        layout.addWidget(self._mode_combo)
        self.setLayout(layout)

    def _connect_child_signals(self) -> None:
        self._clear_button.clicked.connect(self.clear_clicked)
        self._load_project_button.clicked.connect(self.load_project_clicked)
        self._mode_combo.currentTextChanged.connect(self.mode_changed)

    # --- Accessors for ToolbarController ---

    def set_project_name(self, name: str) -> None:
        self._project_label.set_project_name(name)

    def clear_project_name(self) -> None:
        self._project_label.clear_project_name()

    def set_enabled(self, enabled: bool) -> None:
        self._clear_button.setEnabled(enabled)
        # Load Project stays disabled at Level 1; controller manages this at higher levels
        self._mode_combo.setEnabled(enabled)

    def set_clear_enabled(self, enabled: bool) -> None:
        self._clear_button.setEnabled(enabled)

    def set_load_project_enabled(self, enabled: bool) -> None:
        """Enabled at Level 2+."""
        self._load_project_button.setEnabled(enabled)

    def get_mode(self) -> str:
        return self._mode_combo.get_mode()

    def unlock_level(self, level: int) -> None:
        """Unlock modes and controls for the given level."""
        self._mode_combo.set_level(level)
        if level >= 2:
            self._load_project_button.setEnabled(True)

# ui/toolbar/toolbar_component.py