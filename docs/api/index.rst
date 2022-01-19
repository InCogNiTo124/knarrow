.. knarrow documentation master file, created by
   sphinx-quickstart on Wed Sep 29 00:18:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to knarrow's documentation!
===================================
 Shoot a `knarrow` to the knee!

Find a knee/elbow point in 1-dimensional data with a plethora of methods.

Quickstart
__________

::

    >>> from knarrow import find_knee
    >>> find_knee([1, 2, 3, 4, 6])  # use a list
    3
    >>> find_knee((1, 2, 3, 4, 6))  # or a tuple
    3
    >>> import numpy as np
    >>> y = np.array([1.0, 1.05, 1.15, 1.28, 1.30, 2.5, 3.6, 4.9])
    >>> find_knee(y)  # provide just the values
    4
    >>> x = np.arange(8)
    >>> find_knee(x, y)  # or both x and y
    4
    >>> A = np.vstack((x, y))
    >>> A
    array([[0.  , 1.  , 2.  , 3.  , 4.  , 5.  , 6.  , 7.  ],
           [1.  , 1.05, 1.15, 1.28, 1.3 , 2.5 , 3.6 , 4.9 ]])
    >>> find_knee(A)  # works with x in first row, y in the second
    4
    >>> A.T
    array([[0.  , 1.  ],
           [1.  , 1.05],
           [2.  , 1.15],
           [3.  , 1.28],
           [4.  , 1.3 ],
           [5.  , 2.5 ],
           [6.  , 3.6 ],
           [7.  , 4.9 ]])
    >>> find_knee(A.T)  # also works with x in the first column, y in the second column
    4
    >>> find_knee(x, y, smoothing=0.01)  # for better results use cubic spline smoothing
    4

Available methods:

- ``angle``
- ``c_method``
- ``distance``
- ``distance_adjacent``
- ``menger_anchored``
- ``menger_succesive``
- ``ols_swiping``

.. mdinclude:: ../../README.md

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   apidoc/c_method.rst
   apidoc/modules.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
