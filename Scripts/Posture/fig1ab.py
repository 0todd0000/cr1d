'''
Create Fig.1a&b from the main manuscript.
'''


import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import ci1d





#(0) Load posture data:
dir0        = Path( __file__ ).parents[2]                     # Main repository directory
dirProc     = os.path.join(dir0, 'Data', 'Posture', 'Processed') # Processed data directory
fnameNPZ    = os.path.join(dirProc, '2_segmented.npz')
with np.load(fnameNPZ, allow_pickle=True) as Z:
	y,cond  = [Z[s] for s in ['y','cond']]



#(1) Downsample data (first 10 s):
hz0    = 1000    # original sampling frequency
hz     = 10, 1   # downsampled frequencies
trial  = 2
y0     = y[trial, 0 : 10000 : int(1000/hz[0]) ]
y1     = y[trial, 0 : 10000 : int(1000/hz[1]) ]
y0    -= y0.mean(axis=0)  # centered
y1    -= y1.mean(axis=0)  # centered





#(2) Plot:
plt.close('all')
fontname = 'serif'
fig,AX   = plt.subplots(1, 2, figsize=(8,3))
ax0,ax1  = AX.flatten()
alpha    = 0.05
for i,(ax,yy) in enumerate( zip([ax0,ax1], [y0,y1]) ):
	bv     = ci1d.BivariateDataset0D(yy)
	cr     = bv.get_confidence_region(alpha)
	pr     = bv.get_prediction_region(alpha)
	ci2    = bv.get_ci2(alpha)

	bv.plot(ax=ax, ms=5, plot_sample_mean=False, color='k', label='Measurement')
	cr.plot(ax=ax, n=51, color='0.5', lw=2, zorder=9)
	pr.plot(ax=ax, n=51, color='0.8', lw=7, zorder=9)
	ci2.plot(ax=ax, n=51, color='k', lw=2, ls='--', zorder=10)
	
	if ax==ax1:
		leg = ax.legend(loc='lower left', bbox_to_anchor=(-0.2,-0.1))
		plt.setp(leg.get_texts(), name=fontname, size=8)

	ax.text(0.5, 1.05, '10 s @ %d Hz (N = %d time points)' %(hz[i],yy.shape[0]), size=12, name=fontname, ha='center', transform=ax.transAxes)
	plt.setp(ax.get_xticklabels() + ax.get_yticklabels(), size=8, name=fontname)
plt.show()



# plt.savefig( os.path.join( os.path.dirname(__file__), 'figs', 'fig1ab.pdf') )