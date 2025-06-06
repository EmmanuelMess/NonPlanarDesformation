from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QScrollArea

from common.MainLoggerHolder import MAIN_LOGGER, MainLoggerHolder


class LogsWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.text = ""

        self.setWindowTitle("Logs")

        self.logsText = QTextEdit()
        self.logsText.setReadOnly(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setMinimumWidth(80 * 15)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.logsText)

        self.rootLayout = QVBoxLayout()
        self.rootLayout.addWidget(self.scrollArea)

        self.setLayout(self.rootLayout)

        MainLoggerHolder().qtObject.lineLogged.connect(self.onLineLogged)

    @Slot(str)
    def onLineLogged(self, line: str) -> None:
        self.text += line + '\n'
        self.logsText.setText(self.text)