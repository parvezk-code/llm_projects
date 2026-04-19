from controller.app_controller import AppController
from state.session_state import SessionState
from ui.page import PageUI
from ui.sidebar import SidebarUI
from ui.pdf_panel import PDFPanelUI
from ui.chat_panel import ChatPanelUI
from services.auth_service import AuthService
from services.pdf_service import PDFService
from services.llm_service import LLMService


def main() -> None:
    controller = AppController(
        state=SessionState(),
        page_ui=PageUI(),
        sidebar_ui=SidebarUI(),
        pdf_ui=PDFPanelUI(),
        chat_ui=ChatPanelUI(),
        auth_svc=AuthService(),
        pdf_svc=PDFService(),
        llm_svc=LLMService(),
    )
    controller.run()


if __name__ == "__main__":
    main()
