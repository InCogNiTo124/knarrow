from typing import Any

import numpy as np
import numpy.typing as npt

def r_squared(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_]) -> float: ...
def ols_swiping(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], kwargs: Any) -> int: ...
