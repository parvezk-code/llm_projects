# ui/toolbar/widgets/theme_combo_widget.py

from PyQt6.QtWidgets import QComboBox


class ThemeComboWidget(QComboBox):
    """Theme selector. Owns its own styling, data, and population."""

    THEMES = [
        ("Slate Indigo", "theme_01_slate_indigo.qss"),
        ("Forest Green", "theme_02_forest_green.qss"),
        ("Light Amber",  "theme_03_light_amber.qss"),
        ("Light Rose",   "theme_04_light_rose.qss"),
        ("Light Teal",   "theme_05_light_teal.qss"),
        ("Ocean Blue",   "theme_06_ocean_blue.qss"),
        ("Purple Haze",  "theme_07_purple_haze.qss"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup()

    def _setup(self):
        self.setFixedHeight(32)
        self.setObjectName("themeCombo")
        for display_name, _ in self.THEMES:
            self.addItem(display_name)

    def get_filename_at(self, index: int) -> str:
        _, filename = self.THEMES[index]
        return filename