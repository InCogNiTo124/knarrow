Distance method
===============
.. role:: strike
    :class: strike

The distance method finds a knee by searching for the point which is as far as possible from the line going through the point's neighbours.

For every point except for the two edge points, a line is passed through the two points' neighbour points. Then, an orthogonal distance is measured from the point to that line. The point which is the furthest from the line is declared the knee.

This method is quite sensitive to the input noise, so consider smoothing the input with cubic spline smoothing.

Implementation [1]_
****

Let's assume we have three points :math:`P_0(x_0, y_0)`, :math:`P_1(x_1, y_1)` and :math:`P_2(x_2, y_2)`. Let's also assume we want to calculate the distance from the point :math:`P_0` to the line going through :math:`P_1` and :math:`P_2`.

The distance from a point to the line, given a line and the point, as per [2]_ is:

.. math:: \mathrm{distance} \left(P_{1},P_{2},\left(x_{0},y_{0}\right)\right)={\frac {|\left(x_{2}-x_{1}\right)\left(y_{1}-y_{0}\right)-\left(x_{1}-x_{0}\right)\left(y_{2}-y_{1}\right)|}{\sqrt {\left(x_{2}-x_{1}\right)^{2}+\left(y_{2}-y_{1}\right)^{2}}}}

If you really look at the equation, the denominator looks like the length of *some* vector, and the numerator looks kinda like a determinant of *some* matrix. We'll try to express that matrix and that vector using our points.

Let's translate this entire triangle so that :math:`P_1` becomes the origin :math:`O(0, 0)`. This means we now have :math:`P'_1(0, 0)`, :math:`P'_0(x'_0=x_0-x_1, y'_0=y_0-y_1)` and :math:`P'_2(x'_2=x_2-x_1, y'_2=y_2-y_1)`. Rewriting the distance yields:


.. math:: \mathrm{distance} \left(O,P'_{2},\left(x'_{0},y'_{0}\right)\right)={\frac {|\left(x'_2\right)\left(-y'_0\right)-\left(-x'_0\right)\left(y'_2\right)|}{\sqrt {\left(x'_2\right)^{2}+\left(y'_2\right)^{2}}}} = \frac{\left|det\left(\left[\begin{array}{cc}x'_0 & y'_0\\ x'_2 &y'_2\end{array}\right]\right)\right|}{|P'_2|}

The implementation makes use of the derived final form.

#. First, all length 3 consecutive windows are extracted from the input points using fancy NumPy indexing. The middle of the three points acts as the point :math:`P_0`, and the left and right neigbour act as points :math:`P_1` and :math:`P_2`, respectively.
#. Then, :math:`P_1` is subtracted from both :math:`P_0` and :math:`P_2`.
#. The determinant and the (now prime) :math:`P'_2` vector length are computed
#. The determinant is divided with the vector length, yielding the resulting distance

The implementation heavily relies on NumPy broadcasting and indexing, so all computations for all points are performed at once.


.. [1] The implementations are usually not explained in detail, however this implementation uses some mathematical and :code:`numpy` tricks which I'd like to explain
.. [2] https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points