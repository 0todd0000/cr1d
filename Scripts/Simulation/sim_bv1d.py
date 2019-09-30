'''
Validate prediction and confidence regions for bivariate 1D data.

Refer to Appendix F for details regarding the cr1d and spm1d packages, and in particular how to:
1. Simulate random bivariate data
2. Contruct confidence and prediction regions
3. Check whether bivariate points lie within the caluclated regions
'''


import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import cr1d
from spm1d import rft1d


def run_single_iteration(J, fwhm):
	y           = mu + rft1d.random.multirandn1d(J, Q, I, fwhm, W)  # bivariate Gaussian 1D data
	ynew        = mu + rft1d.random.multirandn1d(1, Q, I, fwhm, W)[0]  # an additional random observation
	ds          = cr1d.BivariateDataset1D(y)
	cr          = ds.get_confidence_region(alpha=alpha)
	pr          = ds.get_prediction_region(alpha=alpha)
	ci2         = ds.get_ci2(alpha=alpha)
	in_cr       = cr.isinside(mu)       # mu in confidence region?
	in_pr       = pr.isinside(ynew)     # ynew in prediction region?
	in_ci2      = ci2.isinside(mu)      # mu in CI2?
	ynew_in_ci2 = ci2.isinside(ynew)    # ynew in CI2?
	return in_cr, in_pr, in_ci2, ynew_in_ci2



#(0) Initialize parameters:
np.random.seed(0)        # seed the random number generator to replicate results
alpha   = 0.05       # Type I error rate
J       = np.array([5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200])  # sample sizes
FWHM    = np.array([5, 10, 20, 30, 40, 50])  # smoothness values
Q       = 101        # number of continuum nodes
I       = 2          # number of vector components
mu      = np.zeros((Q,I))  # true population mean
W       = np.eye(2)  # population covariance
niter   = 10000      # number of simulation iterations (set this to 10000 to replicate the paper's results)





#(1) Simulate:
FPR        = []   # false positive rate (outer loop)
for JJ in J:
	fpr    = []   # false positive rate  (inner loop)
	for fwhm in FWHM:
		print('J=%d, FWHM=%d...'%(JJ,fwhm))
		inregion     = np.array([run_single_iteration(JJ, fwhm) for i in range(niter)])
		avg_inregion = inregion.mean(axis=0)
		fpr.append( 1 - avg_inregion )
	FPR.append( fpr )
FPR = np.array(FPR)



#(2) Save results
dir0        = Path( __file__ ).parents[2] # Main repository directory
fnameNPZ    = os.path.join(dir0, 'Data', 'Simulation', 'results1d.npz')   # Simulation results file name
np.savez_compressed(fnameNPZ, fpr=FPR, J=J, FWHM=FWHM)



# #(3) Plot results:
# plt.close('all')
# fig,AX = plt.subplots(2, 2, figsize=(8,6) )
# for i,ax in enumerate( AX.flatten() ):
# 	ax.plot(J, FPR[:,:,i])
# 	ax.legend(['CR', 'PR', 'CI2-mu', 'CI2-new'])
# 	ax.axhline(0.05, color='k', ls=':')
# plt.show()

