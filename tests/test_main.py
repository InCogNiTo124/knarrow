from knarrow.main import (
    angle,
    distance,
    double_triangle_area,
    get_squared_vector_lengths,
    menger_anchored,
    menger_successive,
)
import numpy as np
import pytest

ALL_FUNCTIONS = [angle, menger_anchored, menger_successive, distance]


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


@pytest.mark.parametrize("function", ALL_FUNCTIONS)
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
def test_onevar(function, x, target):
    result = function(x)
    assert isinstance(result, int)
    assert result == target


# im lazy so I copied the inputs from above
# I think I'll need to add more tests soon...
@pytest.mark.parametrize("function", ALL_FUNCTIONS)
@pytest.mark.parametrize(
    "y,target",
    [
        (np.array([1.0, 1.05, 1.15, 1.28, 1.30, 2.5, 3.6, 4.9]), 4),
        (np.array((1, 2, 3, 4, 6)), 3),
        (np.array([1, 2, 3, 4, 5, 7]), 4),
    ],
)
def test_twovar(function, y, target):
    # test normally
    x = np.arange(len(y))
    result = function(x, y)
    assert isinstance(result, int)
    assert result == target

    # test shuffled
    rng = np.random.default_rng()
    random_indices = rng.choice(x, len(x), replace=False)
    print(x, x[random_indices])
    result = function(x[random_indices], y[random_indices])
    assert isinstance(result, int)
    assert result == target


@pytest.mark.xfail(raises=AssertionError)
@pytest.mark.parametrize("function", ALL_FUNCTIONS)
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
def test_fails(function, inputs):
    function(*inputs)
