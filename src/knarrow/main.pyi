from typing import Any, List, Optional

import numpy.typing as npt

_METHODS: List[str]

def find_knee(
    x: npt.ArrayLike,
    y: Optional[npt.ArrayLike] = ...,
    method: str = ...,
    **kwargs: Any,
) -> int: ...

def all(
    x: npt.ArrayLike,
    y: Optional[npt.ArrayLike] = ...,
    **kwargs: Any,
) -> int: ...
