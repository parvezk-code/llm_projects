from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.toolbar.toolbar_component import ToolbarComponent
from ui.toolbar.toolbar_controller import ToolbarController
from ui.status_bar.status_bar_component import StatusBarComponent
from ui.status_bar.status_bar_controller import StatusBarController
from ui.chat_area.chat_area_component import ChatAreaComponent
from ui.chat_area.chat_area_controller import ChatAreaController
from ui.input_bar.input_bar_component import InputBarComponent
from ui.input_bar.input_bar_controller import InputBarController
from ui.ui_bundle import UIBundle


class UIComposer:
    """
    Builds all UI components and their controllers.
    Attaches them to the main window.
    Returns a UIBundle.
    """

    @staticmethod
    def compose(window: QMainWindow) -> UIBundle:
        # ── Central widget + root layout ─────────────────────────────────────
        central = QWidget()
        central.setObjectName("centralWidget")
        window.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Components ────────────────────────────────────────────────────────
        toolbar_comp = ToolbarComponent()
        chat_area_comp = ChatAreaComponent()
        input_bar_comp = InputBarComponent()
        status_bar_comp = StatusBarComponent()

        # ── Layout ────────────────────────────────────────────────────────────
        root.addWidget(toolbar_comp)
        root.addWidget(chat_area_comp, stretch=1)
        root.addWidget(input_bar_comp)
        root.addWidget(status_bar_comp)

        # ── Controllers ───────────────────────────────────────────────────────
        toolbar_ctrl = ToolbarController(toolbar_comp)
        status_bar_ctrl = StatusBarController(status_bar_comp)
        chat_area_ctrl = ChatAreaController(chat_area_comp)
        input_bar_ctrl = InputBarController(input_bar_comp)

        return UIBundle(
            toolbar=toolbar_ctrl,
            status_bar=status_bar_ctrl,
            chat_area=chat_area_ctrl,
            input_bar=input_bar_ctrl,
        )
