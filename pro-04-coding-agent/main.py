import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow
from utils.logger import configure_logging
from conf.settings.config_bundle import load_config
from app.main_controller import MainController


def load_stylesheet(app: QApplication) -> None:
    qss_path = Path(__file__).parent / "styles" / "ocean_blue_theme.qss"
    # qss_path = Path(__file__).parent / "styles" / "main.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text())


def main() -> None:
    configure_logging()

    config = load_config()

    app = QApplication(sys.argv)
    app.setApplicationName(config.app.app_name)

    load_stylesheet(app)

    window = QMainWindow()
    window.setWindowTitle(config.app.app_name)
    window.resize(800, 500)
    window.setMinimumSize(600, 480)

    # MainController builds UI, services, wires everything
    _controller = MainController(window=window, config=config)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
