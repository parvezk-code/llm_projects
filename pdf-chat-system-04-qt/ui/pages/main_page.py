# ui/pages/main_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from ui.components.toolbar.toolbar_component import ToolbarComponent
from ui.components.status_bar.status_bar_component import StatusBarComponent
from ui.components.chat_area.chat_area_component import ChatAreaComponent
from ui.components.input_bar.input_bar_component import InputBarComponent
from ui.components.file_picker.file_picker import FilePickerComponent

from ui.controllers.toolbar_controller import ToolbarController
from ui.controllers.status_bar_controller import StatusBarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.input_bar_controller import InputBarController
from ui.controllers.file_picker_controller import FilePickerController

from ui.ui_bundle import UIBundle


class MainPage(QWidget):
    """
    Default application screen. Assembles components into a vertical layout
    and exposes a UIBundle of their controllers. Contains no business logic.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_components()
        self._create_controllers()
        self._create_layout()
        self._create_bundle()

    def _create_components(self):
        self._toolbar = ToolbarComponent()
        self._status_bar = StatusBarComponent()
        self._chat_area = ChatAreaComponent()
        self._input_bar = InputBarComponent()
        self._file_picker = FilePickerComponent()   # non-visual; not laid out

    def _create_controllers(self):
        self._toolbar_ctrl = ToolbarController(self._toolbar)
        self._status_bar_ctrl = StatusBarController(self._status_bar)
        self._chat_area_ctrl = ChatAreaController(self._chat_area)
        self._input_bar_ctrl = InputBarController(self._input_bar)
        self._file_picker_ctrl = FilePickerController(self._file_picker)

    def _create_layout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._status_bar)
        layout.addWidget(self._chat_area, stretch=1)
        layout.addWidget(self._input_bar)
        self.setLayout(layout)

    def _create_bundle(self):
        self._bundle = UIBundle(
            toolbar=self._toolbar_ctrl,
            status_bar=self._status_bar_ctrl,
            chat_area=self._chat_area_ctrl,
            input_bar=self._input_bar_ctrl,
            file_picker=self._file_picker_ctrl,
        )

    # --- Public ---

    def get_bundle(self) -> UIBundle:
        return self._bundle

# ui/pages/main_page.py
