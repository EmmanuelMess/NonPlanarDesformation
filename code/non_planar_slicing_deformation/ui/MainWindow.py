import os
from typing_extensions import List, Optional, cast

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

import pyvistaqt as pvqt # type: ignore

from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.deformer.Deformer import Deformer
from non_planar_slicing_deformation.ui import Strings
from non_planar_slicing_deformation.ui.DeformerTab import DeformerTab
from non_planar_slicing_deformation.ui.UndeformerTab import UndeformerTab
from non_planar_slicing_deformation.undeformer.Undeformer import Undeformer


class MainWindow(QWidget):

    def __init__(self, configuration: Configuration) -> None:
        super().__init__()

        # State
        self.deformer: Deformer = configuration.deformer()
        self.undeform: Undeformer = configuration.undeformer()

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

        self.deformerTab = DeformerTab(self, configuration)
        self.deformerTab.setVisible(False)

        self.undeformerTab = UndeformerTab(self, configuration)
        self.undeformerTab.setVisible(False)

        self.rootLayout.addLayout(self.topButtonsLayout)
        self.rootLayout.addWidget(self.deformerTab)
        self.rootLayout.addWidget(self.undeformerTab)

        self._showDeformerTab()

    @Slot()
    def onDeformerShow(self):
        self._showDeformerTab()

    @Slot()
    def onUndeformerShow(self):
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


