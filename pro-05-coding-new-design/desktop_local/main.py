# desktop_local/main.py

import sys
from PyQt6.QtWidgets import QApplication

from utils.logger import configure_logging
from conf.settings.config_bundle import load_config
from core.services.chat.plain_chat_service import PlainChatService
from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.main_controller import MainController


def build_local_gateways(config) -> GatewayBundle:
    """LOCAL mode: build Gateways that wrap Core services directly."""
    plain_chat_service = PlainChatService(
        api_key=config.openai.api_key,
        model=config.openai.model,
        temperature=config.openai.llm_temperature,
        max_tokens=config.openai.llm_max_tokens,
    )
    return GatewayBundle(
        chat=ChatGateway(plain_chat_service),
    )


def main() -> None:
    configure_logging()

    app = QApplication(sys.argv)

    try:
        config = load_config()
    except Exception as error:
        print(
            f"Configuration error: {error}\n\n"
            "Set your OpenAI key in conf/env/.env.local:\n"
            "  api_key=sk-...\n"
            "You can copy conf/env/.env.openAI.example as a starting point.",
            file=sys.stderr,
        )
        sys.exit(1)

    app.setApplicationName(config.app.app_name)

    gateways = build_local_gateways(config)     # LOCAL mode decided here only
    controller = MainController(gateways)
    controller.start()                          # builds UI, wires events, applies theme, shows window

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# desktop_local/main.py