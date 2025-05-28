import os
from abc import ABCMeta, abstractmethod

from typing_extensions import Optional, List

from common.MainLogger import MAIN_LOGGER
from configuration.KeyValueParameters import KeyValueParameters
from state.DeformerState import DeformerState


class Undeformer(metaclass=ABCMeta):
    def __init__(self, parameters: KeyValueParameters) -> None:
        self.parameters = parameters
        self.gcode: Optional[List[str]] = None
        self.deformedGcode: Optional[List[str]] = None

    def setGcode(self, gcode: List[str]) -> None:
        self.gcode = gcode

    def undeform(self) -> None:
        if self.gcode is None:
            MAIN_LOGGER.error("Missing gcode, did you forget to call setGcode?")
            return

        self.undeformedGcode = self.undeformImplementation(self.gcode)

    def getUndeformedGcode(self) -> Optional[List[str]]:
        return self.undeformedGcode

    def save(self, path: str) -> None:
        if self.undeformedGcode is None:
            MAIN_LOGGER.error(f"No gcode to save, did you forget to call undeform?")
            return

        if not os.path.splitext(path)[1] == ".gcode":
            MAIN_LOGGER.warn(f"Adding .gcode extension to path '{path}'")
            path += ".gcode"

        with open(path, "w") as file:
            for line in self.undeformedGcode:
                file.write(f"{line}\n")

    @abstractmethod
    def undeformImplementation(self, gcode: List[str]) -> Optional[str]:
        pass

    def getParameters(self) -> KeyValueParameters:
        # TODO move to a superclass
        return self.parameters
