from typing import Any

import numpy as np
import numpy.typing as npt

def r_squared(x: npt.NDArray[np.float64], y: npt.NDArray[np.float64]) -> float: ...
def ols_swiping(x: npt.NDArray[np.float64], y: npt.NDArray[np.float64], **kwargs: Any) -> int: ...
