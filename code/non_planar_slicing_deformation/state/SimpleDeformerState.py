from dataclasses import dataclass

import numpy as np
from typing_extensions import Callable

from state.DeformerState import DeformerState


@dataclass
class SimpleDeformerState(DeformerState):
    rotation: Callable[[np.float64], np.float64]
    offsetsApplied: np.float64