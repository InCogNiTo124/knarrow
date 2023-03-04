# knarrow
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/knarrow)
![PyPI - Downloads](https://img.shields.io/pypi/dm/knarrow)
![PyPI - License](https://img.shields.io/pypi/l/knarrow)
![PyPI](https://img.shields.io/pypi/v/knarrow)
![PyPI - Format](https://img.shields.io/pypi/format/knarrow)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/InCogNiTo124/knarrow)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/InCogNiTo124/knarrow/lint-and-test.yml&branch=master)
![Read the Docs](https://img.shields.io/readthedocs/knarrow)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fknarrow.readthedocs.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Shoot a `knarrow` to the knee ;)

_(The lib is better than this pun, I swear.)_

Detect knee points in various scenarios using a plethora of methods


## Usage
Just plug in your values in a `list`, `tuple` or an `np.ndarray` and watch `knarrow` hit the knee:

```pycon
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
```

### CLI
This library also comes with a handy CLI:
```shell
$ cat data.txt | knarrow
stdin 11
$ cat data.txt | knarrow -o value
stdin 59874.14171519781845532648
$ knarrow --sort -d ',' -o value shuf_delim.txt
shuf_delim.txt 20
```

## Similar projects

While I've come up with most of these methods by myself, I am not the only one. Here is a (non-comprehensive) list of projects I've found that implement a similar funcionality and may have been an inspiration for me:
- [mariolpantunes/knee](https://github.com/mariolpantunes/knee)

Note: this project was bootstrapped by [python-blueprint](https://github.com/johnthagen/python-blueprint)
