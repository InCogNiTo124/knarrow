from knarrow.main import double_triangle_area, get_squared_vector_lengths, menger_successive
import numpy as np
import numpy.typing as npt
import pytest


@pytest.mark.parametrize(
    "vertices,output",
    [
        (np.array([[1.0, 1], [2, 3], [5, 8]]), np.array([5.0, 34, 65])),
    ],
)
def test_get_squared_vector_lenghts(vertices: npt.NDArray[np.float_], output: npt.NDArray[np.float_]) -> None:
    result = get_squared_vector_lengths(vertices)
    assert result.dtype == vertices.dtype
    assert result.shape == output.shape
    assert np.isclose(result, output).all()


@pytest.mark.parametrize(
    "vertices,output",
    [
        (np.array([[1.0, 1], [2, 3], [5, 8]]), np.array(1.0)),
        (np.array([[-1.0, -2], [-3, -4], [-5, -6]]), np.array(0.0)),
        (np.array([[1.0, 2], [0, 4], [9, 7]]), np.array(21)),
    ],
)
def test_double_triangle_area(vertices: npt.NDArray[np.float_], output: npt.NDArray[np.float_]) -> None:
    result = double_triangle_area(vertices)
    assert result.dtype == vertices.dtype
    assert result.shape == output.shape
    assert np.isclose(result, output).all()


@pytest.mark.parametrize(
    "x,target",
    [
        ([1.0, 1.05, 1.15, 1.28, 1.30, 2.5, 3.6, 4.9], 4),
        ((1, 2, 3, 4, 6), 3),
        (np.array([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 7]]), 4),
        (np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 7]]), 4),  # same as above just transposed
        (np.array([1, 2, 3, 4, 6]).reshape(-1, 1), 3),
        (np.array([1, 2, 3, 4, 6]).reshape(1, -1), 3),
    ],
)
def test_menger_onevar(x, target) -> None:
    result = menger_successive(x)
    assert isinstance(result, int)
    assert result == target


@pytest.mark.xfail(raises=AssertionError)
@pytest.mark.parametrize(
    "inputs",
    [
        ([[0.0, 1.0]]),
        ([[0.0, 1.0], [0.0, 1.0]]),
        ([[0.0, 1.0, 2.0], [0.0, 1.0, 2.0], [3.0, 4.0, 5.5]]),
        (np.array([1, 2, 3]).reshape(1, 1, 3),),
        (np.array([[1, 2, 3, 4]]), np.array([[1, 2, 3, 5]])),
        ([0.1, 0.2, 0.3, 0.4, 0.5], [0.2, 0.3, 0.45, 0.60, 1.0, 2.0]),
    ],
)
def test_menger(inputs) -> None:
    menger_successive(*inputs)
