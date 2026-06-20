# ui/screen_manager.py

from ui.main_window import MainWindow
from ui.pages.main_page import MainPage
from ui.ui_bundle import UIBundle


class ScreenManager:
    """
    UI composition root. Selects and builds exactly one screen at startup,
    places it in the main window, and exposes its UIBundle.

    The Main Controller talks only to this object; it never touches
    components, controllers, layouts, or the window directly. There is no
    runtime screen switching: the chosen screen lives for the whole app.
    """

    # Registry of available screens: key -> Page class.
    _PAGES = {
        "main": MainPage,
    }

    def __init__(self, screen: str = "main"):
        self._screen_key = screen
        self._window = MainWindow()
        self._page = None
        self._bundle = None

    def build(self) -> UIBundle:
        """Build the selected screen once and return its controller bundle."""
        page_class = self._select_page_class()
        self._page = page_class()
        self._window.set_page(self._page)
        self._bundle = self._page.get_bundle()
        return self._bundle

    def show(self):
        """Display the main window."""
        self._window.show()

    # --- Internal ---

    def _select_page_class(self):
        if self._screen_key not in self._PAGES:
            raise ValueError(f"Unknown screen: {self._screen_key!r}")
        return self._PAGES[self._screen_key]

# ui/screen_manager.py
