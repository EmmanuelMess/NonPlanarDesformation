from dataclasses import dataclass
from typing_extensions import Callable

from non_planar_desformation.deformer.Deformer import Deformer


@dataclass
class Configuration:
    deformer: Callable[[], Deformer]
    """
    Constructor for the Deformer that will be used in the app
    """

    #undeformer: Callable[[], Undeformer]