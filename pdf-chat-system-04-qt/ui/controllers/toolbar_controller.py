# ui/controllers/toolbar_controller.py

from ui.components.toolbar.toolbar_component import ToolbarComponent


class ToolbarController:
    """Owns the UI-level behavior of the toolbar. Consumes primitives only."""

    def __init__(self, component: ToolbarComponent):
        self._component = component

    # --- Signal binding (one binder per component signal) ---

    def bind_upload_requested(self, handler):
        self._component.upload_clicked.connect(handler)

    def bind_clear_clicked(self, handler):
        self._component.clear_clicked.connect(handler)

    def bind_theme_changed(self, handler):
        self._component.theme_changed.connect(handler)

    # --- Operations (one job each) ---

    def on_pdf_loaded(self, filename: str):
        self._component.set_filename(filename)
        self._component.set_clear_enabled(True)
        self._component.set_clear_state("default")

    def on_chat_cleared(self):
        self._component.set_no_pdf()
        self._component.set_clear_enabled(False)
        self._component.set_clear_state("default")

    def on_chat_updated(self):
        # Reserved no-op: highlight the clear button once a chat is active.
        # self._component.set_clear_state("active")
        pass

    def on_llm_call_failed(self):
        # Reserved no-op: reflect a failed call in the clear button state.
        # self._component.set_clear_state("active")
        pass

# ui/controllers/toolbar_controller.py
