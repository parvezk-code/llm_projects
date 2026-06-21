# desktop/event_handlers/toolbar_event_handler.py

from desktop.action_bundles.action_bundle import ActionBundle


class ToolbarEventHandler:
    """
    Handles events emitted by the toolbar (upload, clear, theme).

    Component controllers are injected, never imported.
    """

    def __init__(
        self,
        actions: ActionBundle,
        file_picker_controller,   # FilePickerController
        toolbar_controller,       # ToolbarController
        chat_area_controller,     # ChatAreaController
        input_bar_controller,     # InputBarController
        status_bar_controller,    # StatusBarController
    ):
        self._actions = actions
        self._file_picker = file_picker_controller
        self._toolbar = toolbar_controller
        self._chat_area = chat_area_controller
        self._input_bar = input_bar_controller
        self._status_bar = status_bar_controller

    def on_upload_clicked(self):
        # Opens the file dialog. The chosen path arrives via the file picker's
        # pdf_selected signal, handled by FilePickerEventHandler.
        self._file_picker.open_pdf()

    def on_clear_clicked(self):
        self._actions.clear_chat.execute()
        self._chat_area.clear_chat()
        self._toolbar.on_chat_cleared()
        self._input_bar.clear_input()
        self._input_bar.disable_input()
        self._status_bar.hide_error()

    def on_theme_changed(self, theme_filename: str):
        # Deferred: applying the .qss theme belongs to the styling pass.
        pass

# desktop/event_handlers/toolbar_event_handler.py