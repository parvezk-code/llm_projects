# desktop/event_handlers/input_bar/send_router_handler.py

from desktop.action_bundles.action_bundle import ActionBundle
from desktop.event_handlers.utils.worker import Worker
from ui.controllers.input_bar_controller import InputBarController
from ui.controllers.chat_area_controller import ChatAreaController
from ui.controllers.status_bar_controller import StatusBarController
from ui.controllers.toolbar_controller import ToolbarController


class SendRouterHandler:
    """
    Handles InputBarComponent.send_triggered.

    send_triggered is permanently wired to on_send(), which reads the current mode
    (a primitive) from the toolbar controller and dispatches to the matching
    single-purpose method. This is the only branch in the whole send flow; it
    grows at L3/L4 with agent/graph methods.

    The action runs on a background Worker thread so the UI stays responsive
    during the LLM call. Success and failure are delivered back on the main
    thread (Actions raise; the Worker routes the exception to _on_error).
    """

    def __init__(
        self,
        actions: ActionBundle,
        input_bar: InputBarController,
        chat_area: ChatAreaController,
        status_bar: StatusBarController,
        toolbar: ToolbarController,
    ) -> None:
        self._actions = actions
        self._input_bar = input_bar
        self._chat_area = chat_area
        self._status_bar = status_bar
        self._toolbar = toolbar
        self._worker: Worker | None = None   # held so it isn't GC'd mid-run

    # --- router ---

    def on_send(self) -> None:
        mode = self._toolbar.get_mode()
        handler = {
            "Simple": self.on_send_plain,
            "RAG": self.on_send_rag,
        }.get(mode, self.on_send_plain)   # default keeps Simple safe
        handler()

    # --- mode methods ---

    def on_send_plain(self) -> None:
        user_text = self._input_bar.get_text()
        if not user_text:
            return
        self._start_send(lambda: self._actions.send_plain.execute(user_text))

    def on_send_rag(self) -> None:
        user_text = self._input_bar.get_text()
        if not user_text:
            return

        # Guard: RAG selected but no project/index loaded yet (handler concern).
        if not self._toolbar.has_project_loaded():
            self._status_bar.show_error("Load a project first to use RAG mode.")
            return

        self._start_send(lambda: self._actions.send_rag.execute(user_text))

    # --- threaded execution ---

    def _start_send(self, method) -> None:
        self._status_bar.hide()
        self._set_busy(True)
        self._worker = Worker(
            method=method,
            on_result=self._on_result,
            on_error=self._on_error,
        )
        self._worker.start()

    def _on_result(self, result) -> None:
        # result is (user_message, assistant_message)
        user_msg, assistant_msg = result
        self._chat_area.add_bubble(role=user_msg.role, content=user_msg.content)
        self._chat_area.add_bubble(role=assistant_msg.role, content=assistant_msg.content)
        self._input_bar.clear_text()
        self._set_busy(False)

    def _on_error(self, error: Exception) -> None:
        # LLM / chat failures → inline error bubble in the chat area
        self._chat_area.add_bubble(role="assistant", content=f"Error: {error}")
        self._set_busy(False)

    def _set_busy(self, busy: bool) -> None:
        self._input_bar.set_enabled(not busy)
        self._toolbar.set_enabled(not busy)

# desktop/event_handlers/input_bar/send_router_handler.py