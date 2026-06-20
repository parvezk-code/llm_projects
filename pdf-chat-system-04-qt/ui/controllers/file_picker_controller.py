# ui/controllers/file_picker_controller.py

from ui.components.file_picker.file_picker import FilePickerComponent


class FilePickerController:
    """
    Controller for FilePickerComponent. Asks the component to open the PDF
    dialog; the result is reported through the component's
    pdf_selected / dialog_canceled signals.
    """

    def __init__(self, component: FilePickerComponent):
        self._component = component

    # --- Signal binding ---

    def bind_pdf_selected(self, handler):
        self._component.pdf_selected.connect(handler)

    def bind_dialog_canceled(self, handler):
        self._component.dialog_canceled.connect(handler)

    # --- Operations ---

    def open_pdf(self):
        self._component.open_pdf()

# ui/controllers/file_picker_controller.py
