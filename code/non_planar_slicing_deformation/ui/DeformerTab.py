from typing_extensions import List, Optional, cast

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QPushButton, QHBoxLayout, QSlider, QLabel

import pyvista as pv
import pyvistaqt as pvqt # type: ignore

from non_planar_slicing_deformation.common import Constants
from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.deformer.Deformer import Deformer
from non_planar_slicing_deformation.ui import Strings


class DeformerTab(QWidget):
    """
    QWidget that draws the deformer view
    """


    def __init__(self, parent: QWidget, configuration: Configuration) -> None:
        super().__init__(parent)

        # State
        self.deformer: Deformer = configuration.deformer()
        #TODO self.undeform: Optional[Undeformer] = None

        # Layout
        self.rootLayout =  QHBoxLayout(self)
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

        self.inputModelButton = QPushButton(Strings.openModel)
        self.inputModelButton.clicked.connect(self.onSelectInputFile)
        self.buttonLayout.addWidget(self.inputModelButton)

        self.outputModelButton = QPushButton(Strings.saveModel)
        self.outputModelButton.clicked.connect(self.onSelectOutputFile)
        self.buttonLayout.addWidget(self.outputModelButton)

        # TODO this is temporary, it needs to be replaced with a proper generic settings system
        # TODO disable settings when no model is loaded
        self.textRadius = QLabel()
        self.textRadius.setText(Strings.deformationFactor)
        self.settingsLayout.addWidget(self.textRadius)

        self.radiusSlider = QSlider(Qt.Orientation.Horizontal)
        self.radiusSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.radiusSlider.setRange(-314, 314)
        self.radiusSlider.setFixedWidth(Constants.widthSettings)
        self.radiusSlider.valueChanged.connect(self.onRadiusChanged)
        self.settingsLayout.addWidget(self.radiusSlider)

        self.inputFileDialog = QFileDialog(self)
        self.inputFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.inputFileDialog.setWindowTitle(Strings.openModel)
        self.inputFileDialog.setMimeTypeFilters(["model/stl"])
        self.inputFileDialog.fileSelected.connect(self.onSelectedInputFile)

        self.outputFileDialog = QFileDialog(self)
        self.outputFileDialog.setFileMode(QFileDialog.FileMode.AnyFile)
        self.outputFileDialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self.outputFileDialog.setWindowTitle(Strings.saveModel)
        self.outputFileDialog.fileSelected.connect(self.onSelectedOutputFile)

    @Slot()
    def onRadiusChanged(self, value: int) -> None:
        self.deformer.getParameters()["radius"] = float(value) / 100
        self._updateDeformedMesh()

    @Slot()
    def onSelectInputFile(self) -> None:
        self.inputFileDialog.open()

    @Slot()
    def onSelectedInputFile(self, path: str) -> None:
        if len(path) == 0:
            MAIN_LOGGER.error("No models selected!")
            return

        loadedMesh: pv.DataObject = pv.read(path)

        if not isinstance(loadedMesh, pv.DataSet):
            MAIN_LOGGER.warn("Model is not a pv.DataSet!")
            return

        self.plotterLeft.clear_actors()
        self.plotterLeft.add_mesh(loadedMesh)

        self.deformer.setMesh(cast(pv.DataSet, loadedMesh))
        self._updateDeformedMesh()

    @Slot()
    def onSelectOutputFile(self) -> None:
        self.outputFileDialog.open()

    @Slot()
    def onSelectedOutputFile(self, path: str) -> None:
        if len(path) == 0:
            MAIN_LOGGER.error("No path chosen!")
            return

        self.deformer.save(path)

    def _updateDeformedMesh(self) -> None:
        self.deformer.deform()
        deformedMesh: Optional[pv.DataSet] = self.deformer.getDeformedMesh()

        if deformedMesh is not None:
            self.plotterRight.clear_actors()
            self.plotterRight.add_mesh(deformedMesh)
        else:
            MAIN_LOGGER.error("Deformed mesh cannot be shown!")