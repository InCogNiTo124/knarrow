# knarrow

Shoot a `knarrow` to the knee ;)

(The lib is better than this pun, I swear.)

Detect knee points in various scenarios using a plethora of methods


## Usage
Just plugin your values in a `list`, `tuple` or an `np.ndarray` and watch `knarrow` hit the knee:

```pycon
>>> from stubs import find_knee
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
```

Note: this project was bootstrapped by [python-blueprint](https://github.com/johnthagen/python-blueprint)
