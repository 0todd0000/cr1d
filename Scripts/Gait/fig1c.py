'''
Create Fig.1c from the main manuscript.
'''


import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import ci1d




#(0) Load gait data:
dir0        = Path( __file__ ).parents[2]                     # Main repository directory
dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
fnameNPZ    = os.path.join(dirProc, '3_registered.npz')
with np.load(fnameNPZ, allow_pickle=True) as Z:
	y,cond,foot = [Z[s] for s in ['y','cond','foot']]
### normalize force units by body weight:
bw          = 64 * 9.812
y          /= bw
### extract all trials, single time point, one foot, normal walking, GRF components Y and Z
i           = (cond==0) & (foot==0)  # normal walking, left foot
ind         = 20   # time point
yy          = y[i,ind,1:]



#(1) Create Bivariate dataset and get regions:
alpha  = 0.05
bv     = ci1d.BivariateDataset0D(yy)
cr     = bv.get_confidence_region(alpha)
pr     = bv.get_prediction_region(alpha)
ci2    = bv.get_ci2(alpha)




#(2) Plot:
plt.close('all')
fontname = 'serif'
fig,ax   = plt.subplots(1, 1, figsize=(6,5))
bv.plot(ax=ax, ms=5, plot_sample_mean=False, color='k', label='Measurement')
cr.plot(ax=ax, n=51, color='0.5', lw=2, zorder=9)
pr.plot(ax=ax, n=51, color='0.8', lw=7, zorder=9)
ci2.plot(ax=ax, n=51, color='k', lw=2, ls='--', zorder=10)
leg = ax.legend(loc='lower left')
ax.text(0.5, 0.95, 'Time = %d %% (N = %d trials)' %(ind, yy.shape[0]), size=12, name=fontname, ha='center', transform=ax.transAxes)
plt.setp(leg.get_texts(), name=fontname, size=8)
plt.setp(ax.get_xticklabels() + ax.get_yticklabels(), size=8, name=fontname)
plt.show()


# plt.savefig( os.path.join( os.path.dirname(__file__), 'figs', 'fig1c.pdf') )