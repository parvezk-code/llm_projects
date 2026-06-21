# ui/style_manager.py

from pathlib import Path

from PyQt6.QtWidgets import QApplication


class StyleManager:
    """
    Loads a .qss theme from ui/styles/ and applies it to the whole
    application. Paths resolve relative to the current working directory
    (the project root), matching how the app is launched.
    """

    def __init__(self, styles_dir: str = "ui/styles"):
        self._styles_dir = Path(styles_dir)

    def apply_theme(self, filename: str):
        path = self._styles_dir / filename
        if not path.exists():
            return
        qss = path.read_text(encoding="utf-8")
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(qss)

# ui/style_manager.py