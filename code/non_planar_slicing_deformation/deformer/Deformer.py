import os
from abc import abstractmethod, ABCMeta
from typing_extensions import Optional

import pyvista as pv

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration.KeyValueParameters import KeyValueParameters


class Deformer(metaclass=ABCMeta):
    """
    Generic class representing a deformation of the mesh
    """

    def __init__(self, parameters: KeyValueParameters) -> None:
        self.parameters = parameters
        self.mesh: Optional[pv.DataSet] = None
        self.deformedMesh: Optional[pv.DataSet] = None

    def setMesh(self, model: pv.DataSet) -> None:
        self.mesh = model

    def save(self, path: str) -> None:
        if self.deformedMesh is None:
            MAIN_LOGGER.error(f"No mesh to save, did you forget to call deform?")
            return

        if not os.path.splitext(path)[1] == ".stl":
            MAIN_LOGGER.warn(f"Adding .stl extension to path '{path}'")
            path += ".stl"

        self.deformedMesh.save(path)

    def getDeformedMesh(self) -> Optional[pv.DataSet]:
        return self.deformedMesh

    def deform(self) -> None:
        if self.mesh is None:
            MAIN_LOGGER.error("Mesh is not set, did you forget to call setMesh?")
            return None

        self.deformedMesh = self.deformImplementation(self.mesh)

    @abstractmethod
    def deformImplementation(self, mesh: pv.DataSet) -> Optional[pv.DataSet]:
        pass

    def getParameters(self) -> KeyValueParameters:
        # TODO move to a superclass
        return self.parameters