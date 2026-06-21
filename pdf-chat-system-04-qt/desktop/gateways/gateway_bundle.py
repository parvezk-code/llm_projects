# desktop/gateways/gateway_bundle.py

from dataclasses import dataclass

from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.pdf_gateway import PDFGateway


@dataclass(frozen=True)
class GatewayBundle:
    """
    Single object holding all gateways. Built by the launcher
    (desktop_local / desktop_remote) and handed to the Main Controller,
    which passes it to the Actions.
    """

    chat: ChatGateway
    pdf: PDFGateway

# desktop/gateways/gateway_bundle.py