# ui/pages/chat_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from ui.toolbar.toolbar_component import ToolbarComponent
from ui.controllers.toolbar_controller import ToolbarController
from ui.folder_picker.folder_picker_component import FolderPickerComponent
from ui.controllers.folder_picker_controller import FolderPickerController
from ui.status_bar.status_bar_component import StatusBarComponent
from ui.controllers.status_bar_controller import StatusBarController
from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.controllers.chat_area_controller import ChatAreaController
from ui.input_bar.input_bar_component import InputBarComponent
from ui.controllers.input_bar_controller import InputBarController
from ui.ui_bundle import UIBundle


class ChatPage:
    """
    Assembles all components and their controllers into the chat screen layout.
    Returns a UIBundle of controllers to the ScreenManager.
    Contains no business logic, no state access, no workflows.
    """

    def build(self, parent: QWidget) -> tuple[QWidget, UIBundle]:
        # --- toolbar ---
        toolbar_component = ToolbarComponent()
        toolbar_controller = ToolbarController(component=toolbar_component)

        # --- folder picker ---
        folder_picker_component = FolderPickerComponent()
        folder_picker_controller = FolderPickerController(component=folder_picker_component)

        # --- status bar ---
        status_bar_component = StatusBarComponent()
        status_bar_controller = StatusBarController(component=status_bar_component)

        # --- chat area ---
        chat_area_component = ChatAreaComponent()
        chat_area_controller = ChatAreaController(component=chat_area_component)

        # --- input bar ---
        input_bar_component = InputBarComponent()
        input_bar_controller = InputBarController(component=input_bar_component)

        # --- layout ---
        page_widget = QWidget(parent)
        layout = QVBoxLayout(page_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(toolbar_component)
        layout.addWidget(status_bar_component)
        layout.addWidget(chat_area_component, stretch=1)
        layout.addWidget(input_bar_component)

        bundle = UIBundle(
            toolbar=toolbar_controller,
            folder_picker=folder_picker_controller,
            status_bar=status_bar_controller,
            chat_area=chat_area_controller,
            input_bar=input_bar_controller,
        )

        return page_widget, bundle

# ui/pages/chat_page.py