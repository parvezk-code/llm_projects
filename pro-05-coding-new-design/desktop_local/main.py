# desktop_local/main.py

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from utils.logger import configure_logging
from conf.settings.config_bundle import load_config
from core.services.chat.plain_chat_service import PlainChatService
from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.main_controller import MainController

from langchain_openai import ChatOpenAI


def load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).resolve().parent.parent / "styles" / "main.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text())


def main() -> None:
    configure_logging()

    # --- config (launcher only) ---
    config = load_config()

    # --- Qt app ---
    app = QApplication(sys.argv)
    app.setApplicationName(config.app.app_name)
    load_stylesheet(app)

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