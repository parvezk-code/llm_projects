# ui/toolbar/widgets/mode_combo_widget.py

from PyQt6.QtWidgets import QComboBox


class ModeComboWidget(QComboBox):
    """
    Mode selector: Simple | RAG | Agent | Graph.
    RAG, Agent, Graph are disabled at Level 1 — present but not selectable.
    """

    MODES = ["Simple", "RAG", "Agent", "Graph"]
    LEVEL_1_ENABLED = {"Simple"}

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("modeCombo")
        self._populate()

    def _populate(self) -> None:
        for mode in self.MODES:
            self.addItem(mode)

    def set_level(self, level: int) -> None:
        """Enable only the modes available at the given level."""
        from PyQt6.QtGui import QStandardItem
        from PyQt6.QtCore import Qt
        model = self.model()
        enabled_modes = self._modes_for_level(level)
        for i, mode in enumerate(self.MODES):
            item: QStandardItem = model.item(i)
            if mode in enabled_modes:
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled)
            else:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def _modes_for_level(self, level: int) -> set:
        if level >= 4:
            return {"Simple", "RAG", "Agent", "Graph"}
        if level >= 3:
            return {"Simple", "RAG", "Agent"}
        if level >= 2:
            return {"Simple", "RAG"}
        return {"Simple"}

    def get_mode(self) -> str:
        return self.currentText()

# ui/toolbar/widgets/mode_combo_widget.py