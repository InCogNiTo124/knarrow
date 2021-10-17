from typing import Any

import numpy as np
import numpy.typing as npt

def get_knee(c: float) -> float: ...
def c_method(x: npt.NDArray[np.float_], y: npt.NDArray[np.float_], method: str, kwargs: Any) -> int: ...
