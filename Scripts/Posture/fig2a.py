'''
Create Fig.2a from the main manuscript.

NOTE: the 3D visualization from the main script was generated
using Blender (blender.org);  this Blender functionality is not
supported in this repository.
'''


import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import ci1d




#(0) Load posture data:
dir0        = Path( __file__ ).parents[2]                        # Main repository directory
dirProc     = os.path.join(dir0, 'Data', 'Posture', 'Processed') # Processed data directory
fnameNPZ    = os.path.join(dirProc, '2_segmented.npz')
with np.load(fnameNPZ, allow_pickle=True) as Z:
	y,cond  = [Z[s] for s in ['y','cond']]
y0       = y[0]    # quiet standing example
y1       = y[10]   # one-leg standing example
y0      -= y0.mean(axis=0) # centered
y1      -= y1.mean(axis=0) # centered



#(1) Compute prediction ellipses:
bv0      = ci1d.BivariateDataset0D(y0)
bv1      = ci1d.BivariateDataset0D(y1)
pe0      = bv0.get_prediction_region()
pe1      = bv1.get_prediction_region()







#(2) Plot:
plt.close('all')
fontname = 'serif'
fig,AX   = plt.subplots(2, 2, figsize=(8,6))
ax2,ax1,ax3,ax0 = AX.flatten()

c0,c1     = 'b', 'r'
xlim      = -0.5, 0.5
ylim      = 0, 1.5
Q         = y0.shape[0]
q         = np.linspace(0, 20, Q)

h00       = ax0.plot(q, y0[:,0], lw=2, color=c0, zorder=0)
h01       = ax0.plot(q, y1[:,0], lw=2, color=c1, zorder=0)
h10       = ax1.plot(q, y0[:,1], lw=2, color=c0, zorder=0)[0]
h11       = ax1.plot(q, y1[:,1], lw=2, color=c1, zorder=0)[0]
h20       = ax2.plot(y0[:,0], y0[:,1], 'o', lw=1, ms=1, color=c0, zorder=1)
h21       = ax2.plot(y1[:,0], y1[:,1], 'o', lw=1, ms=1, color=c1, zorder=0)

pe0.plot(ax2, color=(0.1,0.1,0.4), lw=5)
pe1.plot(ax2, color=c1, lw=5)
pe0.plot_patch(ax2, facecolor=c0, alpha=0.3)
pe1.plot_patch(ax2, facecolor=c1, alpha=0.3)

#datum lines:
ax0.axhline(0, color='k', ls=':')
ax1.axhline(1, color='k', ls=':')
ax2.axhline(0, color='k', ls=':')
ax2.axvline(0, color='k', ls=':')


#labels:
size     = 12
s0,s1,s2 = 'Time  (s)', 'COPx  (mm)', 'COPy  (mm)'
ax0.set_xlabel(s0, size=size);   ax0.set_ylabel(s1, size=size)
ax1.set_xlabel(s0, size=size);   ax1.set_ylabel(s2, size=size)
ax2.set_xlabel(s1, size=size);   ax2.set_ylabel(s2, size=size)
ax1.legend([h10,h11], ['Quiet standing', 'One-legged standing'], loc='upper right')
ax3.set_visible(False)

plt.show()


# plt.savefig( os.path.join( os.path.dirname(__file__), 'figs', 'fig2a.pdf') )


