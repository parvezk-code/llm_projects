# desktop/actions/chat/clear_chat_action.py

from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle


class ClearChatAction:
    """
    Workflow: clear the conversation history from state.
    No gateway call needed — state-only operation.
    """

    def __init__(
        self,
        state: StateController,
        gateways: GatewayBundle,
    ) -> None:
        self._state = state
        # gateways injected for interface consistency; not used at Level 1

    def execute(self) -> None:
        self._state.clear_messages()