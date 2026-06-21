# desktop/event_handlers/file_picker_event_handler.py

from desktop.action_bundles.action_bundle import ActionBundle


class FilePickerEventHandler:
    """
    Handles results from the file picker (pdf_selected / dialog_canceled).

    Component controllers are injected, never imported. The PDFDocument
    returned by the upload Action is unpacked into a primitive here.
    """

    def __init__(
        self,
        actions: ActionBundle,
        toolbar_controller,      # ToolbarController
        input_bar_controller,    # InputBarController
        chat_area_controller,    # ChatAreaController
        status_bar_controller,   # StatusBarController
    ):
        self._actions = actions
        self._toolbar = toolbar_controller
        self._input_bar = input_bar_controller
        self._chat_area = chat_area_controller
        self._status_bar = status_bar_controller

    def on_pdf_selected(self, file_path: str):
        self._status_bar.hide_error()
        try:
            document = self._actions.upload_document.execute(file_path)
            # unpack PDFDocument -> primitive (UI never sees PDFDocument)
            self._toolbar.on_pdf_loaded(document.filename)
            self._chat_area.clear_chat()
            self._input_bar.clear_input()
            self._input_bar.enable_input()
        except Exception as error:
            self._status_bar.show_error(f"Could not load PDF: {error}")

    def on_dialog_canceled(self):
        # Nothing to do when the user cancels the dialog.
        pass

# desktop/event_handlers/file_picker_event_handler.py