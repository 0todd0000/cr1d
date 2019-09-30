'''
Create Fig.2b from the main manuscript.

NOTE: the 3D visualization from the main script was generated
using Blender (blender.org);  this Blender functionality is not
supported in this repository.
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
### extract all trials, one foot, both tasks, GRF components Y and Z
y0          = y[(cond==0)&(foot==0)]
y1          = y[(cond==1)&(foot==0)]
Q           = y.shape[1]








#(2) Plot:
plt.close('all')
fontname = 'serif'
fig,AX   = plt.subplots(2, 2, figsize=(8,6))
ax2,ax1,ax3,ax0 = AX.flatten()
c0,c1    = '0.7', '0.3'
cm0,cm1  = 'b', 'r'
xlim     = -0.5, 0.5
ylim     = 0, 1.5

h00  = ax0.plot(y0[:,:,1].T, lw=1, color=c0, zorder=0)
h01  = ax0.plot(y1[:,:,1].T, lw=1, color=c1, zorder=0)
hm00 = ax0.plot(y0[:,:,1].mean(axis=0), lw=3, color=cm0, zorder=1)
hm01 = ax0.plot(y1[:,:,1].mean(axis=0), lw=3, color=cm1, zorder=1)

h10  = ax1.plot(y0[:,:,2].T, lw=1, color=c0, zorder=0)
h11  = ax1.plot(y1[:,:,2].T, lw=1, color=c1, zorder=0)
hm10 = ax1.plot(y0[:,:,2].mean(axis=0), lw=3, color=cm0, zorder=1)[0]
hm11 = ax1.plot(y1[:,:,2].mean(axis=0), lw=3, color=cm1, zorder=1)[0]
ax1.legend([hm10,hm11], ['Normal', 'Fast'])

h20  = ax2.plot(y0[:,:,1].T, y0[:,:,2].T, lw=1, color=c0, zorder=0)
h21  = ax2.plot(y1[:,:,1].T, y1[:,:,2].T, lw=1, color=c1, zorder=0)
hm20 = ax2.plot(y0[:,:,1].mean(axis=0), y0[:,:,2].mean(axis=0), lw=3, color=cm0, zorder=1)
hm21 = ax2.plot(y1[:,:,1].mean(axis=0), y1[:,:,2].mean(axis=0), lw=3, color=cm1, zorder=1)
plt.setp(ax2, xlim=xlim, ylim=ylim)


#datum lines:
ax0.axhline(0, color='k', ls=':')
ax1.axhline(1, color='k', ls=':')
ax2.axvline(0, color='k', ls=':')

#labels:
size     = 12
s0,s1,s2 = 'Time  (%)', 'GRFx  (BW)', 'GRFy  (BW)'
ax0.set_xlabel(s0, size=size);   ax0.set_ylabel(s1, size=size)
ax1.set_xlabel(s0, size=size);   ax1.set_ylabel(s2, size=size)
ax2.set_xlabel(s1, size=size);   ax2.set_ylabel(s2, size=size)
ax3.set_visible(False)

plt.show()



# plt.savefig( os.path.join( os.path.dirname(__file__), 'figs', 'fig2b.pdf') )


