OLS method
==========

The OLS method fits a varying pair of lines using OLS linear regression

In the first iteration, one of the lines is fit to the :math:`2` points and the other line is fit to the :math:`N-1` points - they share the second point. The sum of their respective coefficients of determination :math:`R^2` is stored as a score.
In the second interation, one of the lines is fit to the :math:`3` points, and the other to the :math:`N-3` points - they share the third point. Again, the sum of :math:`R^2` is stored as a score.

... you get the idea.

The reasoning is, since the knee is the point of maximum curvature, before and after the knee graphs usually look *somewhat* as lines, meaning :math:`R^2` scores should kinda sorta be relatively high. If both lines have high score, there should be a knee there [1]_.

In theory, one could assign different weights to the lines, as to make :math:`x`'s or :math:`y`'s more important. The implementation does not support that, yet.

.. [1] "There should be a knee there", provided they are, indeed, different lines, with different slopes and intercepts.