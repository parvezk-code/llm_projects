# ui/screen_manager.py

from ui.main_window import MainWindow
from ui.pages.chat_page import ChatPage
from ui.ui_bundle import UIBundle


class ScreenManager:
    """
    UI composition root and the only UI object the MainController talks to.
    Builds the page once, places it in the window, returns the controller bundle.
    Owns the window; knows nothing about Event Handlers, Actions, Gateways, Core, or mode.
    """

    def __init__(self) -> None:
        self._window = MainWindow()
        self._bundle: UIBundle | None = None

    def build(self) -> UIBundle:
        """Build the screen, place it in the window, return the controller bundle."""
        page = ChatPage()
        page_widget, bundle = page.build(parent=self._window)
        self._window.setCentralWidget(page_widget)
        self._bundle = bundle
        return bundle

    def show(self) -> None:
        """Display the main window."""
        self._window.show()

# ui/screen_manager.py