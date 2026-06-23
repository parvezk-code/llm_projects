# desktop_local/main.py

import sys
from PyQt6.QtWidgets import QApplication

from utils.logger import configure_logging
from conf.settings.config_bundle import load_config
from core.services.chat.plain_chat_service import PlainChatService
from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.main_controller import MainController
from ui.style_manager import StyleManager

from langchain_openai import ChatOpenAI


def main() -> None:
    configure_logging()

    # --- config (launcher only) ---
    config = load_config()

    # --- Qt app ---
    app = QApplication(sys.argv)
    app.setApplicationName(config.app.app_name)

    # --- apply theme ---
    StyleManager().apply_theme("ocean_blue.qss")

    # --- build core services ---
    llm = ChatOpenAI(
        api_key=config.openai.openai_api_key,
        model=config.openai.openai_model,
        temperature=config.openai.temperature,
        max_tokens=config.openai.max_tokens,
    )
    plain_chat_service = PlainChatService(
        llm=llm,
        system_prompt=config.app.system_prompt,
    )

    # --- build LOCAL gateways ---
    gateways = GatewayBundle(
        chat=ChatGateway(plain_chat_service=plain_chat_service),
    )

    # --- run ---
    controller = MainController(gateways=gateways)
    controller.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()