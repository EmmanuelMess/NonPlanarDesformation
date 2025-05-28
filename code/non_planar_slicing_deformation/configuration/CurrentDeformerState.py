from typing_extensions import Optional, Type

from common.Singleton import Singleton
from state.DeformerState import DeformerState


class CurrentDeformerState(metaclass=Singleton):
    # TODO check that the type is correct by passing a type to the constructor

    def __init__(self, type: Type[DeformerState]=None):
        self.state: Optional[type] = None

    def setState(self, state: DeformerState) -> None:
        self.state = state

    def getState(self) -> Optional[DeformerState]:
        return self.state