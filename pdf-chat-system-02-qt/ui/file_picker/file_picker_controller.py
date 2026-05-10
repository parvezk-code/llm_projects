# ui/file_picker/file_picker_controller.py

from ui.file_picker.file_picker import FilePickerComponent


class FilePickerController:
    """
    Controller for FilePickerComponent.

    It asks the component to open the PDF dialog.
    The selected file path is emitted by the component
    through pdf_selected(file_path).
    """

    def __init__(self, component: FilePickerComponent):
        self._component = component

    def open_pdf(self):
        self._component.open_pdf()

    def bind_pdf_selected(self, handler):
        self._component.pdf_selected.connect(handler)

    def bind_dialog_canceled(self, handler):
        self._component.dialog_canceled.connect(handler)