C-method
========

The *C-method* [1]_ fits a function :math:`f\left(x; c\right) = \frac{x\left(e^c + 1\right)}{x e^c + 1}`, where :code:`x` is your input's :math:`x` coordinates, :code:`y` is your input's :math:`y` coordinates, and :math:`c` is the parameter which is tuned.
The :math:`c` parameter tuning is done with a custom implementation of a `Newton-Raphson method <https://en.wikipedia.org/wiki/Newton%27s_method>`_.

After the optimal :math:`c` is found, the theoretical knee :math:`x*` is located at :math:`x* = \frac{\sqrt{e^c+1}-1}{e^c}`, as per [1]_. The function returns the input :math:`x` coordinate closest to the theoretical knee.

.. [1] The interested reader is invited to take a look at `The C method (blog.msmetko.xyz) <https://blog.msmetko.xyz/posts/2>`_ for the derivation of both of these equations.