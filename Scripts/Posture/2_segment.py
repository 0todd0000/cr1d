'''
Segment imported center of pressure (COP) data.

"Segment" = discard first 5 s, retain next 20 s for analysis
'''

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt


def segment(y, t0=5, durn=20, hz=1000): # starting time, duration, sampling frequency
	i0 = int(t0 * hz)
	i1 = i0 + int( durn * hz )
	return y[i0:i1]
	

# #(0) Segment single trial: (development purposes)
# dir0        = Path( __file__ ).parents[2]                     # Main repository directory
# dirProc     = os.path.join(dir0, 'Data', 'Posture', 'Processed') # Processed data directory
# fnameNPZ    = os.path.join(dirProc, '1_imported.npz')
# with np.load(fnameNPZ, allow_pickle=True) as Z:
# 	y,cond  = [Z[s] for s in ['y','cond']]
# yy          = y[0]
# ys          = segment(yy)
# #plot:
# plt.close('all')
# fig,ax      = plt.subplots(1, 2, figsize=(8,3))
# ax[0].plot(yy);  ax[0].set_title('Raw')
# ax[1].plot(ys);  ax[1].set_title('Segmented')
# plt.show()




# #(1) Segment all:
# dir0        = Path( __file__ ).parents[2]                     # Main repository directory
# dirProc     = os.path.join(dir0, 'Data', 'Posture', 'Processed') # Processed data directory
# fnameNPZ0   = os.path.join(dirProc, '1_imported.npz')
# fnameNPZ1   = os.path.join(dirProc, '2_segmented.npz')
# with np.load(fnameNPZ0, allow_pickle=True) as Z:
# 	y,cond  = [Z[s] for s in ['y','cond']]
# ys          = np.array([segment(yy) for yy in y])
# np.savez_compressed(fnameNPZ1, y=ys, cond=cond)

