Kneedle
=======

Kneedle implements the algorithm described in the [1]_. Not much to say, really.

In short, the algorithm works as follows:

#. (Optionally) Smooth the input using cubic splice smoothing
#. Scale the input to fit into the unit square :math:`\left[0, 1\right] \times \left[0, 1\right]`
#. Calculate the vertical distance of the points from the line :math:`y=x`.
#. Find the points which are local maxima. Such points are taller than their neighbours. These are knee candidates.
#. For each local maximum, define a threshold. The threshold calculation is a hyperparameter of the Kneedle algorithm
#. If there are no other knee candidates over a threshold of a particular knee candidate, then the candidate is the true knee. If there are other knee candidates, then that candidate is discarded.

The output of the algorithm is, usually, at least one knee, and possibly more than one. Sometimes, the curve can be very smooth so no true knee can be found.

.. [1] V. Satopaa, J. Albrecht, D. Irwin and B. Raghavan, "Finding a "Kneedle" in a Haystack: Detecting Knee Points in System Behavior," *2011 31st International Conference on Distributed Computing Systems Workshops*, 2011, pp. 166-171, doi: `10.1109/ICDCSW.2011.20 <https://raghavan.usc.edu/papers/kneedle-simplex11.pdf>`_.