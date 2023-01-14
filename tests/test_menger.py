import numpy as np
import pytest

from knarrow.menger import double_triangle_area, get_squared_vector_lengths


@pytest.mark.parametrize(
    "vertices,output",
    [
        (np.array([[1.0, 1], [2, 3], [5, 8]]), np.array([5.0, 34, 65])),
    ],
)
def test_get_squared_vector_lenghts(vertices, output):
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
def test_double_triangle_area(vertices, output):
    result = double_triangle_area(vertices)
    assert result.dtype == vertices.dtype
    assert result.shape == output.shape
    assert np.isclose(result, output).all()
