# desktop_local/main.py

import sys

from PyQt6.QtWidgets import QApplication

from core.services.llm_service import LLMService
from core.services.pdf_service import PDFService
from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.pdf_gateway import PDFGateway
from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.main_controller import MainController
from desktop_local.config import LLMConfig, load_llm_config


def build_local_gateways(config: LLMConfig) -> GatewayBundle:
    """LOCAL mode: build Gateways that wrap the Core services directly."""
    llm_service = LLMService(
        api_key=config.api_key,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    pdf_service = PDFService()
    return GatewayBundle(
        chat=ChatGateway(llm_service),
        pdf=PDFGateway(pdf_service),
    )


def main():
    app = QApplication(sys.argv)

    config = load_llm_config()
    if not config.api_key:
        print(
            "Warning: OPENAI_API_KEY is not set. PDF upload will work, but chat "
            "requests will fail until you set it.",
            file=sys.stderr,
        )

    gateways = build_local_gateways(config)     # decides LOCAL mode here
    controller = MainController(gateways)
    controller.start()                          # builds UI, wires events, shows window

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# desktop_local/main.py