'''
Validate prediction and confidence intervals for univariate 1D data.
'''


import numpy as np
from matplotlib import pyplot
from spm1d import rft1d
import ci1d


#(0) Initialize parameters:
np.random.seed(0)   #seed the random number generator to replicate results
alpha       = 0.05  #Type I error rate
J           = 10    #sample size
Q           = 101   #number of continuum nodes
fwhm        = 20    #smoothness
mu          = np.zeros(Q)  #true population mean
niterations = 100   #number of datasets / experiments to simulate
in_ci       = []    #list that will hold one True or False value for each iteration
in_pi       = []    #list that will hold one True or False value for each iteration


#(1) Simulate:
for i in range(niterations):
	y       = mu + rft1d.randn1d(J, Q, fwhm) #Gaussian data
	ynew    = mu + rft1d.randn1d(1, Q, fwhm)  #and additional random observation
	ds      = ci1d.UnivariateDataset1D(y)
	ci      = ds.get_confidence_region(alpha=alpha)
	pi      = ds.get_prediction_region(alpha=alpha)
	in_ci.append( ci.isinside(mu) )
	in_pi.append( pi.isinside(ynew) )


#(2) Report:
### confidence region:
prop_in     = np.mean( in_ci )  #proportion of experiments where the true mean lies inside the CI
prop_out    = 1 - prop_in       #proportion of experiments where the true mean lies outside the CI
print('Proportion of random datasets with mu inside CI: %.3f' %prop_in)
print('Proportion of random datasets with mu outside CI: %.3f' %prop_out)
### prediction region:
prop_in     = np.mean( in_pi )  #proportion of experiments where the true mean lies inside the CI
prop_out    = 1 - prop_in       #proportion of experiments where the true mean lies outside the CI
print('Proportion of random datasets with new observation inside PI: %.3f' %prop_in)
print('Proportion of random datasets with new observation outside PI: %.3f' %prop_out)


