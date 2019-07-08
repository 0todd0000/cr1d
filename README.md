# ci1d
A Python package for computing confidence and prediction intervals for 0D and 1D univariate and bivariate data.

This package contains:

* Functions and classes for computing and displaying confidence regions and predictions regions for 0D and 1D datasets
* Scripts for replicating results from the main paper (see below)
* Notebooks for reviewing theory and for standalone, step-by-step calculations

Requirements:

* Python 3.x
* NumPy
* SciPy
* Matplotlib
* [spm1d](http://www.spm1d.org)


Please consider citing:

Pataky TC, Yamagata M, Ichihashi N, Duarte M (in review). Adjustment to: "CI2 for creating and comparing confidence-intervals for time-series bivariate plots" Gait & Posture.


<mark>Note</mark>: **ci1d** does not support ellipsoid or hyperellipsoids calculations for multivariate data, they are not implemented in this package because they cannot be readily visualized.