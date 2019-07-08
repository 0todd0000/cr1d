'''
Validate prediction and confidence intervals for bivariate 0D data.
'''


import numpy as np
from matplotlib import pyplot
import ci1d


#(0) Initialize parameters:
np.random.seed(0)        #seed the random number generator to replicate results
alpha       = 0.05       #Type I error rate
mu          = [0,0]      #true population mean
W           = np.eye(2)  #population covariance
J           = 30         #sample size
I           = 2          #number of vector components
niterations = 1000       #number of datasets / experiments to simulate
in_ci       = []         #list that will hold one True or False value for each iteration
in_pi       = []         #list that will hold one True or False value for each iteration



#(1) Simulate:
for i in range(niterations):
	y       = mu + np.random.multivariate_normal(mu, W, J) #bivariate Gaussian data
	ynew    = mu + np.random.multivariate_normal(mu, W)    #an additional random observation
	ds      = ci1d.BivariateDataset0D(y)
	ci      = ds.get_confidence_region(alpha=alpha)
	pi      = ds.get_prediction_region(alpha=alpha)
	in_ci.append( ci.isinside(mu) )
	in_pi.append( pi.isinside(ynew) )


#(2) Report:
### confidence region:
prop_in     = np.mean( in_ci )  #proportion of experiments where the true mean lies inside the CE
prop_out    = 1 - prop_in       #proportion of experiments where the true mean lies outside the CE
print('Proportion of random datasets with mu inside CE: %.3f' %prop_in)
print('Proportion of random datasets with mu outside CE: %.3f' %prop_out)
### prediction region:
prop_in     = np.mean( in_pi )  #proportion of experiments where the true mean lies inside the PE
prop_out    = 1 - prop_in       #proportion of experiments where the true mean lies outside the PE
print('Proportion of random datasets with new observation inside PE: %.3f' %prop_in)
print('Proportion of random datasets with new observation outside PE: %.3f' %prop_out)


