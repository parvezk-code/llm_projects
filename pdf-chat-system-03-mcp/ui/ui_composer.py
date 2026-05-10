# ui/ui_composer.py

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.toolbar.toolbar_component import ToolbarComponent
from ui.toolbar.toolbar_controller import ToolbarController
from ui.status_bar.status_bar_component import StatusBarComponent
from ui.status_bar.status_bar_controller import StatusBarController
from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.chat_area.chat_area_controller import ChatAreaController
from ui.input_bar.input_bar_component import InputBarComponent
from ui.input_bar.input_bar_controller import InputBarController
from ui.file_picker.file_picker import FilePickerComponent
from ui.file_picker.file_picker_controller import FilePickerController
from ui.ui_bundle import UIBundle


class UIComposer:

    def build(self, window: QMainWindow) -> UIBundle:

        # --- Create components ---
        toolbar_component     = ToolbarComponent()
        status_bar_component  = StatusBarComponent()
        chat_area_component   = ChatAreaComponent()
        input_bar_component   = InputBarComponent()
        file_picker_component = FilePickerComponent()

        # --- Create controllers ---
        toolbar_ctrl    = ToolbarController(toolbar_component)
        status_bar_ctrl = StatusBarController(status_bar_component)
        chat_area_ctrl  = ChatAreaController(chat_area_component)
        input_bar_ctrl  = InputBarController(input_bar_component)
        file_picker_ctrl= FilePickerController(file_picker_component)

        # --- Build main window layout ---
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(toolbar_component)
        layout.addWidget(status_bar_component)
        layout.addWidget(chat_area_component, stretch=1)
        layout.addWidget(input_bar_component)

        central_widget.setLayout(layout)
        window.setCentralWidget(central_widget)
        window.setWindowTitle("Chat PDF")
        window.resize(700, 600)

        # --- Return frozen bundle ---
        return UIBundle(
            toolbar=toolbar_ctrl,
            status_bar=status_bar_ctrl,
            chat_area=chat_area_ctrl,
            input_bar=input_bar_ctrl,
            file_picker=file_picker_ctrl
        )