import pyvistaqt as pvqt  # type: ignore
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from typing_extensions import Optional, List

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.ui import Strings, GcodePlotHelper
from non_planar_slicing_deformation.undeformer.Undeformer import Undeformer


class UndeformerTab(QWidget):
    """
    QWidget that draws the undeformer view
    """

    def __init__(self, parent: QWidget, configuration: Configuration) -> None:
        super().__init__(parent)

        # State
        self.undeformer: Undeformer = configuration.undeformer()

        # Layout
        self.rootLayout = QHBoxLayout(self)
        self.centralLayout = QVBoxLayout(self)
        self.plottersLayout = QHBoxLayout(self)
        self.buttonLayout = QHBoxLayout(self)

        self.settingsLayout = QVBoxLayout(self)
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.rootLayout.addLayout(self.centralLayout)
        self.rootLayout.addLayout(self.settingsLayout)

        # TODO add controls tutorial
        # TODO link both plotters's cameras
        self.plotterLeft = pvqt.QtInteractor()
        self.plottersLayout.addWidget(self.plotterLeft)
        self.plotterRight = pvqt.QtInteractor()
        self.plottersLayout.addWidget(self.plotterRight)

        self.centralLayout.addLayout(self.plottersLayout)
        self.centralLayout.addLayout(self.buttonLayout)

        self.inputModelButton = QPushButton(Strings.openGcode)
        self.inputModelButton.clicked.connect(self.onSelectInputFile)
        self.buttonLayout.addWidget(self.inputModelButton)

        self.outputModelButton = QPushButton(Strings.saveGcode)
        self.outputModelButton.clicked.connect(self.onSelectOutputFile)
        self.buttonLayout.addWidget(self.outputModelButton)

        self.inputFileDialog = QFileDialog(self)
        self.inputFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.inputFileDialog.setWindowTitle(Strings.openModel)
        self.inputFileDialog.setMimeTypeFilters(["application/x-gcode"])
        self.inputFileDialog.fileSelected.connect(self.onSelectedInputFile)

        self.outputFileDialog = QFileDialog(self)
        self.outputFileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        self.outputFileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self.outputFileDialog.setWindowTitle(Strings.saveModel)
        self.outputFileDialog.fileSelected.connect(self.onSelectedOutputFile)

    @Slot()
    def onSelectInputFile(self) -> None:
        self.inputFileDialog.open()

    @Slot()
    def onSelectedInputFile(self, path: str) -> None:
        if len(path) == 0:
            MAIN_LOGGER.error("No models selected!")
            return

        gcode: Optional[List[str]] = None

        with open(path, "rt", encoding="utf-8") as gcodeFile:
            gcode = gcodeFile.readlines()

        if gcode is None:
            MAIN_LOGGER.warning("Gcode did not load")
            return

        self.plotterLeft.clear_actors()
        self.plotterLeft.add_mesh(GcodePlotHelper.plottable3AxisGcode(gcode))

        self.undeformer.setGcode(gcode)
        self._updateUndeformedMesh()

    @Slot()
    def onSelectOutputFile(self) -> None:
        self.outputFileDialog.open()

    @Slot()
    def onSelectedOutputFile(self, path: str) -> None:
        if len(path) == 0:
            MAIN_LOGGER.error("No path chosen!")
            return

        self.undeformer.save(path)

    def _updateUndeformedMesh(self) -> None:
        self.undeformer.undeform()
        undeformedGcode: Optional[List[str]] = self.undeformer.getUndeformedGcode()

        if undeformedGcode is not None:
            self.plotterRight.clear_actors()
            self.plotterRight.add_mesh(GcodePlotHelper.plottable4AxisGcode(undeformedGcode))
        else:
            MAIN_LOGGER.error("Undeformed mesh cannot be shown!")
