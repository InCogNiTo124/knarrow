import numpy as np
import numpy.typing as npt


def np_windowed(length: int, window_size: int, stride: int = 1, dilation: int = 1) -> npt.NDArray[np.int_]:
    base_indices: npt.NDArray[np.int_] = stride * np.arange((length - window_size) // (stride * dilation) + 1).reshape(
        -1, 1
    )
    windows: npt.NDArray[np.int_] = dilation * np.arange(window_size).reshape(1, -1)
    return windows + base_indices  # broadcasting trick


def np_anchored(length: int) -> npt.NDArray[np.int_]:
    indices = list(range(1, length - 1))
    first = [0] * len(indices)
    last = [length - 1] * len(indices)
    return np.stack((first, indices, last), axis=-1)


def prepare(f):  # type: ignore
    def inner(*args, **kwargs):  # type:ignore
        assert 1 <= len(args) <= 2
        if len(args) == 2:
            x = np.array(args[0])
            assert x.ndim == 1 and x.shape[0] > 3
            y = np.array(args[1])
            assert y.ndim == 1 and y.shape[0] > 3
        elif len(args) == 1:
            argument = np.array(args[0]).squeeze()  # squeeze ensures all dimensions are > 1
            assert 1 <= argument.ndim <= 2
            if argument.ndim == 1:
                assert argument.shape[0] >= 3, "The input must have at least 3 points"
                y = argument
                x = np.arange(len(y))
            elif argument.ndim == 2:
                n_rows, n_cols = argument.shape
                if n_rows > n_cols:
                    argument = argument.T
                assert argument.shape[1] >= 3, "The input must have at least 3 points"
                x, y = argument[0], argument[1]
        else:
            raise ValueError("There can only be 1 or 2 positional arguments passed to the function")
        return f(x, y, **kwargs)

    return inner
