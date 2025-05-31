import os
from abc import ABCMeta, abstractmethod

from typing_extensions import Optional, List

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration.KeyValueParameters import KeyValueParameters


class Undeformer(metaclass=ABCMeta):
    """
    Generic class representing an inverse deformation of the gcode (for a mesh deformed by :class:`Deformer`),
    after its sliced
    """

    def __init__(self, parameters: KeyValueParameters) -> None:
        self.parameters = parameters
        self.gcode: Optional[List[str]] = None
        self.undeformedGcode: Optional[List[str]] = None

    def setGcode(self, gcode: List[str]) -> None:
        """
        Set the gcode to undeform
        """
        self.gcode = gcode

    def undeform(self) -> bool:
        """
        Do the undeformation using the gcode and the state
        :return: if successful
        """

        if self.gcode is None:
            MAIN_LOGGER.error("Missing gcode, did you forget to call setGcode?")
            return False

        self.undeformedGcode = self.undeformImplementation(self.gcode)
        return self.undeformedGcode is not None

    def getUndeformedGcode(self) -> Optional[List[str]]:
        """
        Get the result of the undeformation if its available
        :return: The undeformed gcode if its available, otherwise None
        """
        return self.undeformedGcode

    def save(self, path: str) -> None:
        """
        Save the undeformed gcode to a file
        """
        if self.undeformedGcode is None:
            MAIN_LOGGER.error("No gcode to save, did you forget to call undeform?")
            return

        if not os.path.splitext(path)[1] == ".gcode":
            MAIN_LOGGER.warning(f"Adding .gcode extension to path '{path}'")
            path += ".gcode"

        with open(path, "wt", encoding="utf-8") as file:
            for line in self.undeformedGcode:
                file.write(f"{line}\n")

    @abstractmethod
    def undeformImplementation(self, gcode: List[str]) -> Optional[List[str]]:
        """
        Hidden implementation for :func:`~uneform` that subclasses must implement.
        This must not be used outside :class:`Undeformer`.
        """

    def getParameters(self) -> KeyValueParameters:
        """
        Get the :class:`KeyValueParameters` for this Undeformer
        """
        # TODO move to a superclass
        return self.parameters
