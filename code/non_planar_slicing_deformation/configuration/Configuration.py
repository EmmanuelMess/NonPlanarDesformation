from dataclasses import dataclass
from typing_extensions import Callable, Type

from non_planar_slicing_deformation.deformer.Deformer import Deformer
from state.DeformerState import DeformerState
from undeformer.Undeformer import Undeformer


@dataclass
class Configuration:
    deformer: Callable[[], Deformer]
    """
    Constructor for the Deformer that will be used in the app
    """

    undeformer: Callable[[], Undeformer]
    """
    Constructor for the Undeformer that will be used in the app
    """

    stateType: Type[DeformerState]