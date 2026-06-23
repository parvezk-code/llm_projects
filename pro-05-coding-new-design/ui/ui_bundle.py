# ui/ui_bundle.py

from dataclasses import dataclass

from ui.controllers.toolbar_controller import ToolbarController
from ui.controllers.folder_picker_controller import FolderPickerController
from ui.controllers.status_bar_controller import StatusBarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.input_bar_controller import InputBarController


@dataclass(frozen=True)
class UIBundle:
    """
    Immutable bundle of all UI component controllers.
    Returned by ScreenManager.build(), passed to MainController.
    Contains no logic.
    """
    toolbar: ToolbarController
    folder_picker: FolderPickerController
    status_bar: StatusBarController
    chat_area: ChatAreaController
    input_bar: InputBarController

# ui/ui_bundle.py