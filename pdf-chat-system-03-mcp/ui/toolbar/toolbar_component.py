# ui/toolbar/toolbar_component.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from ui.toolbar.widgets.upload_button_widget import UploadButtonWidget
from ui.toolbar.widgets.filename_label_widget import FilenameLabelWidget
from ui.toolbar.widgets.clear_button_widget import ClearButtonWidget
from ui.toolbar.widgets.theme_combo_widget import ThemeComboWidget


class ToolbarComponent(QWidget):
    """
    Composes all toolbar widgets.
    Single responsibility: wire children together
    and expose clean signals upward.
    """

    upload_clicked = pyqtSignal()
    clear_clicked  = pyqtSignal()
    theme_changed  = pyqtSignal(str)  # emits selected theme filename

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_widgets()
        self._create_layout()
        self._connect_child_signals()

    def _create_widgets(self):
        self._upload_btn      = UploadButtonWidget()
        self._filename_label  = FilenameLabelWidget()
        self._clear_btn       = ClearButtonWidget()
        self._theme_combo     = ThemeComboWidget()

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 6, 8, 6)
        layout.addWidget(self._upload_btn)
        layout.addWidget(self._filename_label, stretch=1)
        layout.addWidget(self._clear_btn)
        layout.addWidget(self._theme_combo)
        self.setLayout(layout)

    def _connect_child_signals(self):
        self._upload_btn.clicked.connect(self.upload_clicked)
        self._clear_btn.clicked.connect(self.clear_clicked)
        self._theme_combo.currentIndexChanged.connect(self._on_theme_changed)

    def _on_theme_changed(self, index: int):
        filename = self._theme_combo.get_filename_at(index)
        self.theme_changed.emit(filename)

    # --- Accessors for ToolbarController ---
    def set_filename(self, filename: str):
        self._filename_label.set_filename(filename)

    def set_no_pdf(self):
        self._filename_label.set_no_pdf()

    def set_clear_enabled(self, enabled: bool):
        self._clear_btn.setEnabled(enabled)

    def set_clear_state(self, state: str):
        self._clear_btn.set_state(state)