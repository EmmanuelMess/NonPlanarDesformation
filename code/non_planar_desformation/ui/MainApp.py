import sys

from PySide6 import QtWidgets

from non_planar_desformation.common import Constants
from non_planar_desformation.common.Singleton import Singleton
from non_planar_desformation.configuration.Configuration import Configuration
from non_planar_desformation.ui.MainWindow import MainWindow


class MainApp(metaclass=Singleton):  # pylint: disable=too-few-public-methods
    """
    Initial runner for the app, container for the state of the main Qt runner, and the main window
    """

    def __init__(self, configuration: Configuration) -> None:
        super().__init__()
        self.app = QtWidgets.QApplication([])

        self.mainWindow = MainWindow(configuration)
        self.mainWindow.resize(Constants.width, Constants.height)

    def run(self) -> None:
        """
        Runs the app
        """
        self.mainWindow.show()
        sys.exit(self.app.exec())