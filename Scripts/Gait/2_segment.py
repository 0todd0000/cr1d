'''
Segment the imported ground reaction force (GRF) data from the Gait experiment.

"Segment" = extract the ground reaction force data from the foot-ground contact phase.
'''

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt


def segment(y, th=5, wb=1): # threshold, walk-back
	r         = np.linalg.norm(y, axis=1)   # resultant GRF
	b         = r > th                      # binary hit-miss for resultant force exceeding threshold
	ind       = np.argwhere(b).flatten()    # all indices meeting the criterion
	i0,i1     = ind[0]-wb, ind[-1]+wb+1     # starting and ending frames
	return y[i0:i1]
	

# #(0) Segment single trial: (development purposes)
# dir0        = Path( __file__ ).parents[2]                     # Main repository directory
# dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
# fnameNPZ    = os.path.join(dirProc, '1_imported.npz')
# with np.load(fnameNPZ, allow_pickle=True) as Z:
# 	y,cond,foot = [Z[s] for s in ['y','cond','foot']]
# yy          = y[0]
# ys          = segment(yy)
# #plot:
# plt.close('all')
# fig,ax      = plt.subplots(1, 2, figsize=(8,3))
# ax[0].plot(yy);  ax[0].set_title('Raw')
# ax[1].plot(ys);  ax[1].set_title('Segmented')
# plt.show()



#(1) Segment all:
dir0        = Path( __file__ ).parents[2]                     # Main repository directory
dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
fnameNPZ0   = os.path.join(dirProc, '1_imported.npz')
fnameNPZ1   = os.path.join(dirProc, '2_segmented.npz')
with np.load(fnameNPZ0, allow_pickle=True) as Z:
	y,cond,foot = [Z[s] for s in ['y','cond','foot']]
ys          = np.array([segment(yy, th=30, wb=1) for yy in y])
np.savez_compressed(fnameNPZ1, y=ys, cond=cond, foot=foot)




# #(2) Check segmentation:  (development purposes)
# dir0        = Path( __file__ ).parents[2]                     # Main repository directory
# dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
# fnameNPZ    = os.path.join(dirProc, '2_segmented.npz')
# with np.load(fnameNPZ, allow_pickle=True) as Z:
# 	y,cond,foot = [Z[s] for s in ['y','cond','foot']]
# #plot:
# plt.close('all')
# fig,AX  = plt.subplots(2, 2, figsize=(8,6))
# colors  = 'b', 'g', 'r'
# for ax,c,f in zip(AX.flatten(), [0,0,1,1], [0,1,0,1] ):
# 	ind = (cond==c) & (foot==f)
# 	yy  = y[ind]
# 	for ii in range(3):
# 		for yyy in yy:
# 			ax.plot(yyy[:,ii], color=colors[ii])
# plt.show()

