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

    def setMesh(self, mesh: pv.DataSet) -> None:
        """
        Set the input mesh to deform
        """
        self.mesh = mesh

    def save(self, path: str) -> None:
        """
        Save deformed mesh to an stl file
        :param path: A path with ending in a name with or without stl extension
        :return:
        """

        if self.deformedMesh is None:
            MAIN_LOGGER.error("No mesh to save, did you forget to call deform?")
            return

        if not os.path.splitext(path)[1] == ".stl":
            MAIN_LOGGER.warning(f"Adding .stl extension to path '{path}'")
            path += ".stl"

        self.deformedMesh.save(path)

    def getDeformedMesh(self) -> Optional[pv.DataSet]:
        """
        Get a reference to the deformed mesh if it was correctly created
        """
        return self.deformedMesh

    def deform(self) -> bool:
        """
        Deform the mesh, this can fail
        :return: if successful
        """
        if self.mesh is None:
            MAIN_LOGGER.error("Mesh is not set, did you forget to call setMesh?")
            return False

        self.deformedMesh = self.deformImplementation(self.mesh)

        return self.deformedMesh is not None

    @abstractmethod
    def deformImplementation(self, mesh: pv.DataSet) -> Optional[pv.DataSet]:
        """
        Hidden implementation for :func:`~deform` that subclasses must implement.
        This must not be used outside :class:`Deformer`.
        """

    def getParameters(self) -> KeyValueParameters:
        """
        Get the :class:`KeyValueParameters` for this Deformer
        """
        # TODO move to a superclass
        return self.parameters
