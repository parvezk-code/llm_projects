# desktop/actions/chat/clear_chat_action.py

from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle


class ClearChatAction:
    """
    Workflow: reset the session — clears chat history, the loaded project, and
    its index. After this the app is back to a clean Simple-mode state.
    State-only operation — no gateway call.
    """

    def __init__(self, state: StateController, gateways: GatewayBundle) -> None:
        self._state = state
        # gateways injected for interface consistency; not used here

    def execute(self) -> None:
        self._state.reset_on_clear_chat()

# desktop/actions/chat/clear_chat_action.py