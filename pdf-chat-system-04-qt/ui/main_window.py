# ui/main_window.py

from PyQt6.QtWidgets import QMainWindow, QWidget


class MainWindow(QMainWindow):
    """
    Top-level application window. A dumb shell that holds a single central
    widget (the selected page). Contains no components or business logic.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()

    def _setup(self):
        self.setWindowTitle("Chat PDF")
        self.resize(700, 600)

    def set_page(self, page: QWidget):
        self.setCentralWidget(page)

# ui/main_window.py
