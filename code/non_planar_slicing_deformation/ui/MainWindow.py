from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from typing_extensions import Optional

from non_planar_slicing_deformation.common import Constants
from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.ui import Strings
from non_planar_slicing_deformation.ui.DeformerTab import DeformerTab
from non_planar_slicing_deformation.ui.UndeformerTab import UndeformerTab


class MainWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.resize(Constants.width, Constants.height)

        self.configuration: Optional[Configuration] = None

        # Layout
        self.rootLayout = QVBoxLayout(self)

        self.topButtonsLayout = QHBoxLayout(self)
        self.topButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.settingsLayout = QVBoxLayout(self)
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.deformerButton = QPushButton(Strings.deformer)
        self.deformerButton.setCheckable(True)
        self.deformerButton.clicked.connect(self.onDeformerShow)

        self.undeformerButton = QPushButton(Strings.undeformer)
        self.undeformerButton.setCheckable(True)
        self.undeformerButton.clicked.connect(self.onUndeformerShow)

        self.topButtonsLayout.addWidget(self.deformerButton)
        self.topButtonsLayout.addWidget(self.undeformerButton)

        self.deformerTab = DeformerTab(self)
        self.deformerTab.setVisible(False)

        self.undeformerTab = UndeformerTab(self)
        self.undeformerTab.setVisible(False)

        self.rootLayout.addLayout(self.topButtonsLayout)
        self.rootLayout.addWidget(self.deformerTab)
        self.rootLayout.addWidget(self.undeformerTab)

        self._showDeformerTab()

    def setConfiguration(self, configuration: Configuration) -> None:
        self.configuration = configuration

        self.deformerTab.setConfiguration(self.configuration)
        self.undeformerTab.setConfiguration(self.configuration)

    @Slot()
    def onDeformerShow(self) -> None:  # pylint: disable=missing-function-docstring
        self._showDeformerTab()

    @Slot()
    def onUndeformerShow(self) -> None:  # pylint: disable=missing-function-docstring
        self._showUndeformerTab()

    def _showDeformerTab(self) -> None:
        self.deformerButton.setChecked(True)
        self.undeformerButton.setChecked(False)

        self.deformerTab.setVisible(True)
        self.undeformerTab.setVisible(False)

    def _showUndeformerTab(self) -> None:
        self.deformerButton.setChecked(False)
        self.undeformerButton.setChecked(True)

        self.deformerTab.setVisible(False)
        self.undeformerTab.setVisible(True)
