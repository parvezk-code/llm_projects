# ui/toolbar/widgets/mode_combo_widget.py

from PyQt6.QtWidgets import QComboBox


class ModeComboWidget(QComboBox):

    MODES = ["Simple", "RAG", "Agent"]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("modeCombo")
        for mode in self.MODES:
            self.addItem(mode)

    def get_mode(self) -> str:
        return self.currentText()