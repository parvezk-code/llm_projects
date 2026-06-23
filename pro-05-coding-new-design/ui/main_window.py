# ui/main_window.py

from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """
    Top-level window shell.
    Sets title and size only — no components, no logic.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Coding Agent")
        self.setMinimumSize(900, 650)

# ui/main_window.py