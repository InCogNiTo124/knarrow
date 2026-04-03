from typing import Any

import numpy as np
import numpy.typing as npt

def distance(x: npt.NDArray[np.float64], y: npt.NDArray[np.float64], **kwargs: Any) -> int: ...
def distance_adjacent(x: npt.NDArray[np.float64], y: npt.NDArray[np.float64], **kwargs: Any) -> int: ...
