from dataclasses import dataclass

import numpy as np
from typing_extensions import Optional


@dataclass
class FastMove:
    """
    Represents the code G00 of gcode
    """
    position: np.ndarray
    command: str
    extrusion: Optional[float]
    inverseTimeFeed: Optional[float]
    moveLength: float
