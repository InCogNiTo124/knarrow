Distance method
===============
.. role:: strike
    :class: strike

The distance method finds a knee by searching for the point which is as far as possible from the line connecting the first coordinate pari and the last coordinate pair.

Since :code:`knarrow` scales the input to fit inside a square :math:`\left[0, 1\right]\times\left[0, 1\right]`, this effectively means finding a point which is furthest from the line :math:`y=x`.

If you plugin a point :math:`(x_0, y_0)` in the equation, and play with the :strike:`numbers` letters, you'll arrive at a conclusion that the *perpendicular* distance from a point to a line is proportional to the *vertical* distance with a factor of :math:`\sqrt{2}`.

:code:`knarrow` makes use of the fact that the scaling factor does not matter when finding the maximum distance, provided that the factor is strictyl positive, which :math:`\sqrt{2}` surely is. Therefore, the implementation searches for the maximum of :math:`y-x`.