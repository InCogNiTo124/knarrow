---
title: 'knarrow: versatile knee/elbow point locator'
tags:
  - Python
  - optimization
  - curvature
  - knee point search
  - elbow point search
  - preision
  - recall
  - optimal thresholding
authors:
  - name: Marijan Smetko
    orcid: 0000-0001-9457-6761
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 21 February 2022
bibliography: paper.bib
---

# Summary

Optimizing an operating point of a given system does not consist solely of minimization and maximization.[@kneedle] Quite often, a point of diminishing returns is reached, where further changes of a system's hyperparameter do not yield enough performance increase - the system is said to have reached a point of diminishing returns. After such points, the extra resource expenses are not worth the gains. Since we often don't wish to optimize the performance unconditionally, it is important to use methods which evaluate the performance increase with respect to the increase in resource expenditure. The output of such methods is a point in which further changes do not have as much of an effect - the so called _knee points_ or _elbow points_.

![Figure 1: A typical trade-off curves. A balancing point, a.k.a. a knee, might be found at 30% for the blue curve and below 20% for the red curve. Source: http://ncss.com](https://www.ncss.com/wp-content/uploads/2013/01/ROC-Curve-21.png)

# Statement of need

`knarrow` is a Python package which provides the users with a possibility to detect knee points in their (one-dimensional) data. Since there is no "free lunch"[@nfl] for optimization, `knarrow` library provides several methods with different inductive biases which allow the users to use the one which performs the best on their data. It is a product of countless hours and various aproaches to the question: "How exactly to define a point of diminishing returns, also known as a knee or an elbow?".

However, real world is full of noise and inputting raw data like that doesn't usually ends well. This is why `knarrow` also implements a custom cubic spline smoothing algorithm [@Reinsch1967; @Craven1978] to remove as much noise as possible.

`knarrow` is designed to be used by anyone who wishes to optimize the behaviour of their system:

* Finding an optimal TPR/FPR threshold
* Finding the maximum requests-per-second point after which the system's latency skyrockets
* Finding the least amount of money beyond which the performance starts to seriously suffer

... and many other unmentioned applications. `knarrow` is yet to be recognized by the public, however it is successfully used by the author himself in his day-to-day job, mainly for the uses they described above.

# Knee-finding methods

## Angle method
Find a knee by looking at the maximum change of the angle of the line going through consecutive point pairs.

## The C method
This is the author's own, mathemathically derived method. It defines a curve family parametrized by a shape parameter `c`. Since the knee of a curve can be shown to be dependent solely on the shape parameter `c`, the optimal value for `c` is found by the Newton-Raphson method.

## The vertical distance method
Finds a knee by finding which point is the most distance from the line `y=x`.

## Kneedle method
Finds the knee using a custom, optimized implementation of the Kneedle[@kneedle] algorithm.

## Menger method
Find a point in which the menger curvature of a graph has its absolute maximum.

## OLS method
Find a knee by fitting two lines using OLS.

# Acknowledgements

The author acknowledges using various other Internet sources as an inspiration for making `knarrow`. However, [mariolpantunes/knee](https://github.com/mariolpantunes/knee) stands out in particular as a good starting point for this project. This project never applied nor received any financial support.

# References