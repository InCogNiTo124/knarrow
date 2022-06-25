Menger curvature
================

This method traverses the points 3-by-3 and calculates a sort-of-a "score" for each successive triplet. That score is actually the `Menger curvature <https://en.wikipedia.org/wiki/Menger_curvature>`_. The Menger curvature is defined as the inverse of the radius of the circle circumscribed through three points. The rationale is that the knee is the point with maximum curvature, and there is a small asumption that the discrete points are a good approximation of the true underlying function.

There are two types of calculations performed, based on the way of sampling the triplets:

#. Successive Menger Curvature - this slides the length-3 window accross the input points. This method is somewhat sensitive to the noise in the input so use with pure or smoothed data.
#. Anchored Menger Curvature - in this type, the first point, :math:`\left(0, 0\right)`, and the last point, :math:`\left(1, 1\right)`, are always present, and only the middle point is changing. This is somewhat more resilient to noise, however it's a bit slower.

The implementation, just like most of the other methods, uses advanced NumPy, with some math in the background to improve the calculation performance, such as expressing the area of the triangle with matrix determinant etc.