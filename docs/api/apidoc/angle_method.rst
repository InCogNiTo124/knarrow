Angle method
============
The angle method simply checks for a maximal change in the angle of a line passing through consecutive pairs of points. The knee is the point where the angle changes the most.

A quick rundown of an algorithm:

#. For each of the :math:`N-1` consecutive pairs of points, a line which passes through them is calculated
#. For each of the :math:`N-1` lines, an angle inclination is calculated. Angle inclination is the angle formed by the intersection of the line and the :math:`x` axis
#. Assuming the input is type 2, as per :ref:`knee_types_label`, the angles will first start at around :math:`-\frac\pi2` and they will gradually approach :math:`0`.
#. This change, however, is not linear. Around the knee the change is the largest, so by finding the greatest change of the angle value, we find a knee.

The code implements this algorithm in a slightly optimized and vectorized way. However, the algorithm is quite sensitive to the noisy data and it is advised to use cubic spline smoothing before using this method.
