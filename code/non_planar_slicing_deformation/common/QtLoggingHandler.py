import logging

from PySide6.QtCore import Signal, QObject
from typing_extensions import override


class QtLoggingHandler(logging.Handler, QObject):
    lineLogged = Signal(str)

    def __init__(self, parent: QObject) -> None:
        logging.Handler.__init__(self)
        QObject.__init__(self, parent)

    @override
    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        self.lineLogged.emit(message)
