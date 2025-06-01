from typing_extensions import Optional

from non_planar_slicing_deformation.common.Singleton import Singleton
from non_planar_slicing_deformation.state.DeformerState import DeformerState


class CurrentDeformerState(metaclass=Singleton):
    """
    Singleton that provides the current deformer state for the undeformer algorithm
    """
    # TODO check that the type is correct by passing a type to the constructor

    def __init__(self) -> None:
        self.state: Optional[DeformerState] = None

    def setState(self, state: DeformerState) -> None:  # pylint: disable=missing-function-docstring
        self.state = state

    def getState(self) -> Optional[DeformerState]:  # pylint: disable=missing-function-docstring
        return self.state
