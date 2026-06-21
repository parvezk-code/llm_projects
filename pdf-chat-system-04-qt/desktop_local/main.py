# desktop_local/main.py

import sys

from PyQt6.QtWidgets import QApplication

from core.services.llm_service import LLMService
from core.services.pdf_service import PDFService
from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.pdf_gateway import PDFGateway
from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.main_controller import MainController
from conf.settings.openai_config import OpenAIConfig
from conf.settings.config_bundle import load_config


def build_local_gateways(openai_config: OpenAIConfig) -> GatewayBundle:
    """LOCAL mode: build Gateways that wrap the Core services directly."""
    llm_service = LLMService(
        api_key=openai_config.api_key,
        model=openai_config.model,
        temperature=openai_config.llm_temperature,
        max_tokens=openai_config.llm_max_tokens,
    )
    pdf_service = PDFService()
    return GatewayBundle(
        chat=ChatGateway(llm_service),
        pdf=PDFGateway(pdf_service),
    )


def main():
    app = QApplication(sys.argv)

    try:
        config = load_config()
    except Exception as error:
        print(
            "Configuration error: "
            f"{error}\n\n"
            "Set your OpenAI key in conf/env/.env.local (or conf/env/.env.openAI):\n"
            "  api_key=sk-...\n"
            "You can copy conf/env/.env.openAI.example as a starting point.",
            file=sys.stderr,
        )
        sys.exit(1)

    gateways = build_local_gateways(config.openai)   # decides LOCAL mode here
    controller = MainController(gateways)
    controller.start()                               # builds UI, wires events, shows window

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# desktop_local/main.py