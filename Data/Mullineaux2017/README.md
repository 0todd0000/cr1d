
These data are from Mullineaux (2017), Fig.3d.

These data are redistributed with permission of the author.

Mullineaux DR. CI2 for creating and comparing confidence-intervals for time-series bivariate plots. Gait & Posture. 2017 Feb 1;52:367-73. https://doi.org/10.1016/j.gaitpost.2016.12.028



The attached MAT and NPZ files contain two data variables:

* rA : (36, 151, 2) array containing Standard treadmill data

* rB : (40, 151, 2) array containing Curved treadmill data


The data array sizes are (J,Q,I) where:

* J = sample size
* Q = number of time nodes
* I = number of vector components (I=2; ankle,knee)


Figure 3d from Mullineaux (2017) can be reproduced with the following Matlab code:

xAin    = rA(:,:,1)';
yAin    = rA(:,:,2)';
xBin    = rB(:,:,1)';
yBin    = rB(:,:,2)';

g       = 1;
p       = 0.95;
plotyes ='yes';

CI2(xAin, yAin, xBin, yBin, p, g, plotsyes, 15);