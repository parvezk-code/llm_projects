# main.py

import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow
from app.main_controller import MainController
from utils.logger import configure_logging

log = logging.getLogger(__name__)

def main():
    configure_logging()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = QMainWindow()
    apply_theme(app, "theme_06_ocean_blue.qss")
    controller = MainController(window)
    controller.ui.toolbar._component.theme_changed.connect(
        lambda filename: apply_theme(app, filename)
    )
    window.show()
    sys.exit(app.exec())

def apply_theme(app: QApplication, filename: str) -> None:
    try:
        with open(f"styles/{filename}", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        log.warning("Theme file not found: %s", filename)

if __name__ == "__main__":
    main()