# ui/ui_bundle.py

from dataclasses import dataclass

from ui.controllers.toolbar_controller import ToolbarController
from ui.controllers.status_bar_controller import StatusBarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.input_bar_controller import InputBarController
from ui.controllers.file_picker_controller import FilePickerController


@dataclass(frozen=True)
class UIBundle:
    """Immutable bundle of all component controllers, handed to the Main Controller."""

    toolbar: ToolbarController
    status_bar: StatusBarController
    chat_area: ChatAreaController
    input_bar: InputBarController
    file_picker: FilePickerController

# ui/ui_bundle.py
