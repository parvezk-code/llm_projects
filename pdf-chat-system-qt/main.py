# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from app.main_controller import MainController


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = QMainWindow()
    controller = MainController(window)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()