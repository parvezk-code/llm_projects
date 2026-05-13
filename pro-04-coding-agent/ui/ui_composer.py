# ui/ui_composer.py

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from ui.ui_bundle import UIBundle
from ui.toolbar.toolbar_component import ToolbarComponent
from ui.toolbar.toolbar_controller import ToolbarController
from ui.status_bar.status_bar_component import StatusBarComponent
from ui.status_bar.status_bar_controller import StatusBarController
from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.chat_area.chat_area_controller import ChatAreaController
from ui.input_bar.input_bar_component import InputBarComponent
from ui.input_bar.input_bar_controller import InputBarController


class UIComposer:

    def compose(self, window: QMainWindow) -> UIBundle:

        # --- toolbar ---
        toolbar_component = ToolbarComponent()
        toolbar_controller = ToolbarController(component=toolbar_component)

        # --- status bar ---
        status_bar_component = StatusBarComponent()
        status_bar_controller = StatusBarController(component=status_bar_component)

        # --- chat area ---
        chat_area_component = ChatAreaComponent()
        chat_area_controller = ChatAreaController(component=chat_area_component)

        # --- input bar ---
        input_bar_component = InputBarComponent()
        input_bar_controller = InputBarController(component=input_bar_component)

        # --- build main window layout ---
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(toolbar_component)
        layout.addWidget(status_bar_component)
        layout.addWidget(chat_area_component, stretch=1)
        layout.addWidget(input_bar_component)

        window.setCentralWidget(central_widget)

        return UIBundle(
            toolbar=toolbar_controller,
            status_bar=status_bar_controller,
            chat_area=chat_area_controller,
            input_bar=input_bar_controller,
        )