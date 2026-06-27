# desktop/event_handlers/folder_picker/folder_selected_handler.py

import os
from desktop.action_bundles.action_bundle import ActionBundle
from desktop.event_handlers.utils.worker import Worker
from ui.controllers.toolbar_controller import ToolbarController
from ui.controllers.input_bar_controller import InputBarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.status_bar_controller import StatusBarController


class FolderSelectedHandler:
    """
    Handles FolderPickerComponent.folder_selected.

    Builds the project index (load_project action) on a background Worker thread
    so the UI stays responsive during the slow extraction → chunking → embedding
    → vector-store pipeline. On success: set the project label, enable input,
    clear chat. On failure: dismissible status-bar banner.
    """

    def __init__(
        self,
        actions: ActionBundle,
        toolbar: ToolbarController,
        input_bar: InputBarController,
        chat_area: ChatAreaController,
        status_bar: StatusBarController,
    ) -> None:
        self._actions = actions
        self._toolbar = toolbar
        self._input_bar = input_bar
        self._chat_area = chat_area
        self._status_bar = status_bar
        self._worker: Worker | None = None   # held so it isn't GC'd mid-run

    def on_folder_selected(self, path: str) -> None:
        if not path:
            return

        self._status_bar.hide()
        self._set_busy(True)
        self._worker = Worker(
            method=lambda: self._actions.load_project.execute(path),
            on_result=self._on_result,
            on_error=self._on_error,
        )
        self._worker.start()

    def _on_result(self, index) -> None:
        # Unpack domain model (ProjectIndex) to primitives before touching the UI
        self._set_busy(False)
        self._toolbar.reset_on_project_loaded(os.path.basename(index.project_path))
        self._chat_area.reset_on_project_loaded()

    def _on_error(self, error: Exception) -> None:
        # File / load failures → dismissible status-bar banner
        self._status_bar.show_error(f"Failed to load project: {error}")
        self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        self._input_bar.set_enabled(not busy)
        self._toolbar.set_enabled(not busy)

# desktop/event_handlers/folder_picker/folder_selected_handler.py