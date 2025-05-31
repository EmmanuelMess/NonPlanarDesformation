import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from typing_extensions import Dict

from non_planar_slicing_deformation.common.Singleton import Singleton
from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.deformer.SimpleDeformer import SimpleDeformer
from non_planar_slicing_deformation.ui.MainWindow import MainWindow
from non_planar_slicing_deformation.ui.Mode import Mode
from non_planar_slicing_deformation.ui.ModeSelectorWindow import ModeSelectorWindow
from non_planar_slicing_deformation.undeformer.SimpleUndeformer import SimpleUndeformer


class MainApp(metaclass=Singleton):
    """
    Initial runner for the app, container for the state of the main Qt runner, and the main window
    """

    _CONFIGURATION: Dict[Mode, Configuration] = {
        Mode.FOUR_AXIS_SIMPLE: Configuration(deformer=SimpleDeformer, undeformer=SimpleUndeformer),
        # Mode.FOUR_S: None,
        # Mode.THREE_D_PRINTER: None,
    }

    def __init__(self) -> None:
        super().__init__()
        self.app = QtWidgets.QApplication([])

        self.selectorWindow = ModeSelectorWindow()
        self.selectorWindow.accepted.connect(self.onAccepted)

        self.mainWindow = MainWindow()

    def run(self) -> None:
        """
        Runs the app
        """

        self.selectorWindow.show()
        sys.exit(self.app.exec())

    @Slot(Mode)
    def onAccepted(self, mode: Mode) -> None:
        self.mainWindow.setConfiguration(self._CONFIGURATION[mode])

        self.mainWindow.show()
