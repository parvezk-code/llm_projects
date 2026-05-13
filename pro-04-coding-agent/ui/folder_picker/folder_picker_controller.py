# ui/folder_picker/folder_picker_controller.py

from PyQt6.QtCore import QObject

from ui.folder_picker.folder_picker_component import FolderPickerComponent


class FolderPickerController(QObject):
    """
    Manages FolderPickerComponent.
    Exposes open() to trigger folder selection dialog.
    Exposes bind methods for external signal wiring.
    """

    def __init__(self, component: FolderPickerComponent) -> None:
        super().__init__()
        self._component = component

    # --- bind methods ---

    def bind_folder_selected(self, method) -> None:
        self._component.folder_selected.connect(method)

    # --- operation methods ---

    def open(self) -> None:
        self._component.open()