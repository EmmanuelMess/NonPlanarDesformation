from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton
from typing_extensions import List

from ui import Strings
from ui.Mode import Mode


class ModeSelectorWindow(QWidget):
    """
    A mode selector for different printer and deformer configurations
    """

    @dataclass
    class Item:
        mode: Mode
        text: str

    _OPTIONS: List[Item] = [
        Item(Mode.FOUR_AXIS_SIMPLE, Strings.fourAxisSimple),
        # Item(Mode.FOUR_S, Strings.fourS),
        # Item(Mode.THREE_D_PRINTER, Strings.threeAxis)
    ]

    accepted = Signal(Mode)


    def __init__(self) -> None:
        super().__init__()

        self.resize(250, 300)

        self.rootLayout = QVBoxLayout(self)
        self.rootLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.modeText = QLabel()
        self.modeText.setText(Strings.selectMode)

        self.modeDropDown = QComboBox()
        self.modeDropDown.addItems([option.text for option in self._OPTIONS])

        self.acceptButton = QPushButton()
        self.acceptButton.setText(Strings.accept)
        self.acceptButton.pressed.connect(self.onPressedAccept)

        self.rootLayout.addWidget(self.modeText)
        self.rootLayout.addWidget(self.modeDropDown)
        self.rootLayout.addWidget(self.acceptButton)

    @Slot()
    def onPressedAccept(self) -> None:
        selected = self._OPTIONS[self.modeDropDown.currentIndex()]
        self.accepted.emit(selected.mode)
        self.close()
