from dataclasses import dataclass

import numpy as np
from typing_extensions import Optional


@dataclass
class SlowMove:
    """
    Represents the code G01 of gcode
    """
    position: np.ndarray
    command: str
    extrusion: Optional[float]
    inverseTimeFeed: Optional[float]
    moveLength: float
    startPosition: np.ndarray
    endPosition: np.ndarray
    unsegmentedMoveLength: float
