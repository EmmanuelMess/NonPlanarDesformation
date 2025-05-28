import os
from typing_extensions import List, Optional, cast

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

import pyvistaqt as pvqt # type: ignore

from non_planar_slicing_deformation.configuration.Configuration import Configuration
from non_planar_slicing_deformation.deformer.Deformer import Deformer
from non_planar_slicing_deformation.ui import Strings
from ui.DeformerTab import DeformerTab
from ui.UndeformerTab import UndeformerTab
from undeformer.Undeformer import Undeformer


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
        self.deformerButton.clicked.connect(self.onDeformerShow)

        self.undeformerButton = QPushButton(Strings.undeformer)
        self.undeformerButton.clicked.connect(self.onUndeformerShow)

        self.topButtonsLayout.addWidget(self.deformerButton)
        self.topButtonsLayout.addWidget(self.undeformerButton)

        self.deformerTab = DeformerTab(self, configuration)
        self.deformerTab.setVisible(True)

        self.undeformerTab = UndeformerTab(self, configuration)
        self.undeformerTab.setVisible(False)

        self.rootLayout.addLayout(self.topButtonsLayout)
        self.rootLayout.addWidget(self.deformerTab)
        self.rootLayout.addWidget(self.undeformerTab)

    @Slot()
    def onDeformerShow(self):
        self.deformerTab.setVisible(True)
        self.undeformerTab.setVisible(False)

    @Slot()
    def onUndeformerShow(self):
        self.deformerTab.setVisible(False)
        self.undeformerTab.setVisible(True)
