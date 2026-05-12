import logging
from app.models.state.app_state import AppState
from app.models.services.llm_transaction.chat_message import ChatMessage
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
    2. Add user message bubble + save to AppState
    3. Disable input while waiting
    4. Build ChainRequest from AppState
    5. Start ChainWorker (background QThread)
    6. On result  → add assistant bubble, save to AppState, re-enable input
    7. On error   → show error in status bar, re-enable input
    """

    def __init__(
        self,
        state: AppState,
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
        self._state.messages.append(ChatMessage(role="user", content=user_text))

        # ── 3. Disable input while waiting ───────────────────────────────────
        self._ui.input_bar.set_enabled(False)
        self._ui.toolbar.set_clear_enabled(False)

        # ── 4. Build ChainRequest ─────────────────────────────────────────────
        # Pass history EXCLUDING the just-added user message —
        # the user_input is sent separately as the current turn.
        history = self._state.messages[:-1]

        request = ChainRequest(
            system_prompt=self._system_prompt,
            history=history,
            user_input=user_text,
        )

        # ── 5. Start background worker ────────────────────────────────────────
        self._worker = ChainWorker(self._services.chain_controller, request)
        self._worker.result_ready.connect(self._on_result)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()

    def _on_result(self, answer: str) -> None:
        logger.debug("SendMessageHandler: received answer len=%d", len(answer))

        # ── 6. Show assistant bubble ─────────────────────────────────────────
        self._ui.chat_area.add_bubble("assistant", answer)

        # Save assistant message to state
        self._state.messages.append(ChatMessage(role="assistant", content=answer))

        # Re-enable UI
        self._ui.input_bar.set_enabled(True)
        self._ui.toolbar.set_clear_enabled(True)

    def _on_error(self, error: str) -> None:
        logger.error("SendMessageHandler: error=%s", error)

        # ── 7. Show error ─────────────────────────────────────────────────────
        self._state.error = error
        self._ui.status_bar.show_error(error)

        # Remove last user message from state (turn didn't complete)
        if self._state.messages and self._state.messages[-1].role == "user":
            self._state.messages.pop()

        # Re-enable UI
        self._ui.input_bar.set_enabled(True)
        has_messages = bool(self._state.messages)
        self._ui.toolbar.set_clear_enabled(has_messages)
