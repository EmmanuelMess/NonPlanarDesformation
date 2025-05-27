import os
from abc import abstractmethod, ABCMeta
from typing_extensions import Optional

import pyvista as pv

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration.KeyValueParameters import KeyValueParameters


class Deformer(metaclass=ABCMeta):
    def __init__(self, parameters: KeyValueParameters):
        self.parameters = parameters
        self.model: Optional[pv.DataObject] = None
        self.deformedMesh: Optional[pv.DataObject] = None

    def setMesh(self, model: pv.DataObject):
        self.model = model

    def getMesh(self) -> Optional[pv.DataObject]:
        return self.model

    def save(self, path: str) -> None:
        if self.deformedMesh is None:
            MAIN_LOGGER.error(f"No mesh to save!")
            return

        if not os.path.splitext(path)[1] == ".stl":
            MAIN_LOGGER.warn(f"Adding .stl extension to path '{path}'")
            path += ".stl"

        self.deformedMesh.save(path)

    def getDeformedMesh(self) -> Optional[pv.DataSet]:
        return self.deformedMesh

    def deform(self) -> None:
        self.deformedMesh = self.deformImplementation()

    @abstractmethod
    def deformImplementation(self) -> Optional[pv.DataObject]:
        pass

    def getParameters(self) -> KeyValueParameters:
        return self.parameters