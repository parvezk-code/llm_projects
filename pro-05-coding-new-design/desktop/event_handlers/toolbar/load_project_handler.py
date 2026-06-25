# desktop/event_handlers/toolbar/load_project_handler.py

from ui.controllers.folder_picker_controller import FolderPickerController


class LoadProjectHandler:
    """
    Handles ToolbarComponent.load_project_clicked.
    Single responsibility: open the folder-picker dialog. The actual indexing
    happens in FolderSelectedHandler once a folder is chosen.
    """

    def __init__(self, folder_picker: FolderPickerController) -> None:
        self._folder_picker = folder_picker

    def on_load_project_clicked(self) -> None:
        self._folder_picker.open()

# desktop/event_handlers/toolbar/load_project_handler.py