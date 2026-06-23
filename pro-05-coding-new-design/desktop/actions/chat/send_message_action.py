# desktop/actions/chat/send_message_action.py

import logging
from core.models.chat_message import ChatMessage, Role
from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle

logger = logging.getLogger(__name__)


class SendMessageAction:
    """
    Workflow: send a user message and receive an AI response.

    1. Set is_processing = True (reset in finally).
    2. Read history from state and build the provider message list here
       (system prompt + history as dicts + new user turn). ChatMessage→dict
       conversion belongs in the Action, not in the model or gateway.
    3. Call gateway.get_reply(messages).
    4. Commit BOTH the user and assistant ChatMessages to state only after
       a successful reply (atomic — a failed call leaves state unchanged).
    5. Return (user_message, assistant_message) to the Event Handler.
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

            logger.debug("SendMessageAction: input=%r", user_text)
            reply_text = self._gateways.chat.get_reply(messages)
            logger.debug("SendMessageAction: reply length=%d", len(reply_text))

            user_msg = ChatMessage.user(user_text)
            assistant_msg = ChatMessage.assistant(reply_text)

            # Commit both atomically — only reached if get_reply succeeded
            self._state.add_chat_message(user_msg)
            self._state.add_chat_message(assistant_msg)

            return user_msg, assistant_msg

        except Exception:
            logger.exception("SendMessageAction: failed — state unchanged")
            raise
        finally:
            self._state.set_processing(False)

    def _build_messages(self, history: list[ChatMessage], user_text: str) -> list[dict]:
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": Role.USER, "content": user_text})
        return messages

# desktop/actions/chat/send_message_action.py