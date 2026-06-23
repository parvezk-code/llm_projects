# ui/controllers/folder_picker_controller.py

from PyQt6.QtCore import QObject

from ui.folder_picker.folder_picker_component import FolderPickerComponent


class FolderPickerController(QObject):
    """
    Manages FolderPickerComponent.
    Exposes open() to trigger folder selection dialog.
    Used at Level 2+ (RAG / Agent / Graph modes).
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

# ui/controllers/folder_picker_controller.py