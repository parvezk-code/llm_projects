# ui/ui_bundle.py

from dataclasses import dataclass

from ui.toolbar.toolbar_controller import ToolbarController
from ui.folder_picker.folder_picker_controller import FolderPickerController
from ui.status_bar.status_bar_controller import StatusBarController
from ui.chat_area.chat_area_controller import ChatAreaController
from ui.input_bar.input_bar_controller import InputBarController


@dataclass(frozen=True)
class UIBundle:
    """
    Frozen dataclass holding refs to all UI component controllers.
    Returned by UIComposer, passed to MainController.
    """
    toolbar: ToolbarController
    folder_picker: FolderPickerController
    status_bar: StatusBarController
    chat_area: ChatAreaController
    input_bar: InputBarController