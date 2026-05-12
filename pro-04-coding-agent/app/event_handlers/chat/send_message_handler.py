# app/event_handlers/chat/send_message_handler.py

import logging
from app.state.state_controller import StateController
from app.event_handlers.transformers.chain.history_transformer import convert_history
from services.chain.request import ChainRequest
from services.chain.worker import ChainWorker
from services.service_bundle import ServiceBundle
from ui.ui_bundle import UIBundle

logger = logging.getLogger(__name__)


class SendMessageHandler:
    """
    Handles a single chat turn.

    Steps:
    1. Read user input from input bar
    2. Show user bubble + save to state via StateController
    3. Disable input while waiting
    4. Transform history and build ChainRequest
    5. Start ChainWorker (background QThread)
    6. On result  → add assistant bubble, save to state, re-enable input
    7. On error   → show error in status bar, roll back user message, re-enable input
    """

    def __init__(
        self,
        state: StateController,
        ui: UIBundle,
        services: ServiceBundle,
        system_prompt: str,
    ) -> None:
        self._state = state
        self._ui = ui
        self._services = services
        self._system_prompt = system_prompt
        self._worker: ChainWorker | None = None

    def handle(self) -> None:
        user_text = self._ui.input_bar.get_text()
        if not user_text:
            return

        logger.debug("SendMessageHandler: user_input='%s'", user_text[:60])

        # ── 1. Show user bubble ──────────────────────────────────────────────
        self._ui.input_bar.clear_text()
        self._ui.chat_area.add_bubble("user", user_text)
        self._ui.status_bar.hide()

        # ── 2. Save user message to state ────────────────────────────────────
        self._state.add_message("user", user_text)

        # ── 3. Disable input while waiting ───────────────────────────────────
        self._ui.input_bar.set_enabled(False)
        self._ui.toolbar.set_clear_enabled(False)

        # ── 4. Transform history and build ChainRequest ───────────────────────
        # History excludes the just-added user message —
        # the user_input is sent separately as the current turn.
        history_messages = self._state.get_messages()[:-1]
        lc_history = convert_history(history_messages)

        request = ChainRequest(
            system_prompt=self._system_prompt,
            history=lc_history,
            user_input=user_text,
        )

        # ── 5. Start background worker ────────────────────────────────────────
        self._worker = ChainWorker(self._services.chain_controller, request)
        self._worker.result_ready.connect(self._on_result)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()

    def _on_result(self, answer: str) -> None:
        logger.debug("SendMessageHandler: received answer len=%d", len(answer))

        # ── 6. Show assistant bubble and save to state ───────────────────────
        self._ui.chat_area.add_bubble("assistant", answer)
        self._state.add_message("assistant", answer)

        # Re-enable UI
        self._ui.input_bar.set_enabled(True)
        self._ui.toolbar.set_clear_enabled(True)

    def _on_error(self, error: str) -> None:
        logger.error("SendMessageHandler: error=%s", error)

        # ── 7. Show error and roll back user message ──────────────────────────
        self._state.set_error(error)
        self._ui.status_bar.show_error(error)

        # Roll back user message — turn did not complete
        self._state.pop_last_message()

        # Re-enable UI
        self._ui.input_bar.set_enabled(True)
        self._ui.toolbar.set_clear_enabled(self._state.has_messages())