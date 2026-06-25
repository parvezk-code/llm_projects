# desktop/gateways/gateway_bundle.py

from dataclasses import dataclass
from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.index_gateway import IndexGateway


@dataclass(frozen=True)
class GatewayBundle:
    """
    Immutable bundle of all gateways.
    Built by the launcher; passed to MainController.

    Level 2: adds the IndexGateway for the RAG pipeline.
    """
    chat: ChatGateway
    index: IndexGateway

# desktop/gateways/gateway_bundle.py