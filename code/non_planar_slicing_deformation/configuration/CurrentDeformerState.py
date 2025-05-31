from typing_extensions import Optional, Type

from non_planar_slicing_deformation.common.Singleton import Singleton
from non_planar_slicing_deformation.state.DeformerState import DeformerState


class CurrentDeformerState(metaclass=Singleton):
    # TODO check that the type is correct by passing a type to the constructor

    def __init__(self, stateType: Type[DeformerState] = None):
        self.state: Optional[stateType] = None

    def setState(self, state: DeformerState) -> None:
        self.state = state

    def getState(self) -> Optional[DeformerState]:
        return self.state
