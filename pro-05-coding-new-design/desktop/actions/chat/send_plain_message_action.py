# desktop/actions/chat/send_plain_message_action.py

import logging
from core.models.chat_message import ChatMessage, Role
from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle

logger = logging.getLogger(__name__)


class SendPlainMessageAction:
    """
    Workflow: plain (non-RAG) chat — send a user message, get an AI reply.
    Single-purpose: no mode branching here (the handler routes to this action).

    1. Set is_processing (reset in finally).
    2. Read history, shape provider messages (system + history + user turn).
    3. Call chat gateway (plain path).
    4. Commit both messages atomically only on success.
    5. Return (user_message, assistant_message).
    """

    SYSTEM_PROMPT = (
        "You are an expert Python coding assistant. "
        "Help the user write, review, debug, and improve Python code."
    )

    def __init__(self, state: StateController, gateways: GatewayBundle) -> None:
        self._state = state
        self._gateways = gateways

    def execute(self, user_text: str) -> tuple[ChatMessage, ChatMessage]:
        self._state.set_processing(True)
        try:
            history = self._state.get_chat_messages()
            messages = self._build_messages(history, user_text)

            logger.debug("SendPlainMessageAction: input=%r", user_text)
            reply_text = self._gateways.chat.get_reply(messages)
            logger.debug("SendPlainMessageAction: reply length=%d", len(reply_text))

            user_msg = ChatMessage.user(user_text)
            assistant_msg = ChatMessage.assistant(reply_text)

            self._state.add_message_on_send(user_msg, assistant_msg)

            return user_msg, assistant_msg

        except Exception:
            logger.exception("SendPlainMessageAction: failed — state unchanged")
            raise
        finally:
            self._state.set_processing(False)

    def _build_messages(self, history: list[ChatMessage], user_text: str) -> list[dict]:
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": Role.USER, "content": user_text})
        return messages

# desktop/actions/chat/send_plain_message_action.py