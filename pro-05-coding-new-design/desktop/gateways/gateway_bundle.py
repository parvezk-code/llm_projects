# desktop/gateways/gateway_bundle.py

from dataclasses import dataclass
from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.index_gateway import IndexGateway
from desktop.gateways.agent_gateway import AgentGateway


@dataclass(frozen=True)
class GatewayBundle:
    """
    Immutable bundle of all gateways.
    Built by the launcher; passed to MainController.

    Level 2: adds IndexGateway (RAG pipeline).
    Level 3: adds AgentGateway (tool-using agent).
    """
    chat: ChatGateway
    index: IndexGateway
    agent: AgentGateway

# desktop/gateways/gateway_bundle.py