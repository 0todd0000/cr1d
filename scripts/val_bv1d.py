'''
Validate prediction and confidence intervals for bivariate 1D data.
'''


import numpy as np
from matplotlib import pyplot
import ci1d
from spm1d import rft1d


#(0) Initialize parameters:
np.random.seed(0)        #seed the random number generator to replicate results
alpha       = 0.05       #Type I error rate
J           = 8          #sample size
Q           = 101        #number of continuum nodes
I           = 2          #number of vector components
fwhm        = 25         #smoothness
mu          = np.zeros((Q,I))  #true population mean
W           = np.eye(2)  #population covariance
niterations = 800        #number of datasets / experiments to simulate
in_cr       = []         #list that will hold one True or False value for each iteration
in_pr       = []         #list that will hold one True or False value for each iteration


#(1) Simulate:
for i in range(niterations):
	if i%100 == 0:
		print('Iteration %d...' %i)
	y       = mu + rft1d.random.multirandn1d(J, Q, I, fwhm, W)  #bivariate Gaussian 1D data
	ynew    = mu + rft1d.random.multirandn1d(1, Q, I, fwhm, W)[0]  #an additional random observation
	ds      = ci1d.BivariateDataset1D(y)
	cr      = ds.get_confidence_region(alpha=alpha)
	pr      = ds.get_prediction_region(alpha=alpha)
	in_cr.append( cr.isinside(mu) )
	in_pr.append( pr.isinside(ynew) )


#(2) Report:
### confidence region:
prop_in     = np.mean( in_cr )  #proportion of experiments where the true mean lies inside the CE
prop_out    = 1 - prop_in       #proportion of experiments where the true mean lies outside the CE
print('Proportion of random datasets with mu inside CE: %.3f' %prop_in)
print('Proportion of random datasets with mu outside CE: %.3f' %prop_out)
### prediction region:
prop_in     = np.mean( in_pr )  #proportion of experiments where the true mean lies inside the PE
prop_out    = 1 - prop_in       #proportion of experiments where the true mean lies outside the PE
print('Proportion of random datasets with new observation inside PE: %.3f' %prop_in)
print('Proportion of random datasets with new observation outside PE: %.3f' %prop_out)

