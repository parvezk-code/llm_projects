# desktop/actions/chat/clear_chat_action.py

from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle


class ClearChatAction:
    """
    Workflow: reset the session to its initial state.

    Clears the conversation AND removes the active document, matching the
    old UI where 'Clear' returned the toolbar to the "No PDF loaded" state.
    (If 'Clear' should instead keep the PDF and wipe only the chat, drop the
    clear_document() call.)

    Takes no gateways — it only mutates state.
    """

    def __init__(self, state_controller: StateController, gateways: GatewayBundle):
        self._state = state_controller
        self._gateways = gateways

    def execute(self) -> None:
        self._state.clear_chat()
        self._state.clear_document()

# desktop/actions/chat/clear_chat_action.py