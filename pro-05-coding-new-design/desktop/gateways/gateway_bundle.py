# desktop/gateways/gateway_bundle.py

from dataclasses import dataclass
from desktop.gateways.chat_gateway import ChatGateway


@dataclass(frozen=True)
class GatewayBundle:
    """
    Immutable bundle of all gateways.
    Built by the launcher; passed to MainController.
    """
    chat: ChatGateway