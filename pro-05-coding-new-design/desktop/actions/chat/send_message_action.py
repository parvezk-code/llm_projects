# desktop/actions/chat/send_message_action.py

import logging
from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle

logger = logging.getLogger(__name__)


class SendMessageAction:
    """
    Workflow: send a user message and get an AI response.
    1. Write user message to state.
    2. Read history (excluding current message) from state.
    3. Call ChatGateway.
    4. On success: write assistant message to state, return answer string.
    5. On failure: roll back user message, re-raise so handler can show error.
    """

    def __init__(
        self,
        state: StateController,
        gateways: GatewayBundle,
    ) -> None:
        self._state = state
        self._gateways = gateways

    def execute(self, user_input: str) -> str:
        logger.debug("SendMessageAction: input=%r", user_input)

        self._state.add_message(role="user", content=user_input)
        history = self._state.get_messages()[:-1]  # history excluding current message

        try:
            answer = self._gateways.chat.send(
                history=history,
                user_input=user_input,
            )
        except Exception:
            logger.exception("SendMessageAction: failed, rolling back state")
            self._state.pop_last_message()
            raise

        logger.debug("SendMessageAction: success, answer length=%d", len(answer))
        self._state.add_message(role="assistant", content=answer)
        return answer