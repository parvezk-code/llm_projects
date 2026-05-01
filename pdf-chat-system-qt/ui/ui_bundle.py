# ui/ui_bundle.py

from dataclasses import dataclass
from ui.toolbar.toolbar_controller import ToolbarController
from ui.status_bar.status_bar_controller import StatusBarController
from ui.chat_area.chat_area_controller import ChatAreaController
from ui.input_bar.input_bar_controller import InputBarController
from ui.file_picker.file_picker_controller import FilePickerController


@dataclass(frozen=True)
class UIBundle:
    toolbar:        ToolbarController
    status_bar:     StatusBarController
    chat_area:      ChatAreaController
    input_bar:      InputBarController
    file_picker:    FilePickerController