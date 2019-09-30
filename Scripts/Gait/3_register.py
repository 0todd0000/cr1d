'''
Register the segmented ground reaction force (GRF) data from the Gait experiment.

"Register" = temporally align. Here simple linear interpolation (101 nodes) is used.
'''


import os
from pathlib import Path
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt



def interp1d(y, n=101):
	'''
	Linearly interpolate continuum "y" to "n" equally spaced points
	'''
	t0   = np.arange(y.size)
	t1   = np.linspace(0, y.size-1, n)
	f    = interpolate.interp1d(t0, y, 'linear')
	return f(t1)



# #(0) Register single trial:  (development purposes)
# dir0        = Path( __file__ ).parents[2]                     # Main repository directory
# dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
# fnameNPZ    = os.path.join(dirProc, '2_segmented.npz')
# with np.load(fnameNPZ, allow_pickle=True) as Z:
# 	y,cond,foot = [Z[s] for s in ['y','cond','foot']]
# yy          = y[0]
# yr          = np.array([interp1d(yyy, n=101)  for yyy in yy.T]).T
# #plot:
# plt.close('all')
# plt.figure( figsize=(8,6) )
# ax = plt.axes()
# ax.plot(yr)
# plt.show()



# #(1) Register all:
# dir0        = Path( __file__ ).parents[2]                     # Main repository directory
# dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
# fnameNPZ0   = os.path.join(dirProc, '2_segmented.npz')
# fnameNPZ1   = os.path.join(dirProc, '3_registered.npz')
# with np.load(fnameNPZ0, allow_pickle=True) as Z:
# 	y,cond,foot = [Z[s] for s in ['y','cond','foot']]
# yr          = np.array([[interp1d(yyy, n=101)  for yyy in yy.T] for yy in y]).swapaxes(1, 2)
# np.savez_compressed(fnameNPZ1, y=yr, cond=cond, foot=foot)



#(2) Check registration:  (development purposes)
dir0        = Path( __file__ ).parents[2]                     # Main repository directory
dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
fnameNPZ    = os.path.join(dirProc, '3_registered.npz')
with np.load(fnameNPZ, allow_pickle=True) as Z:
	y,cond,foot = [Z[s] for s in ['y','cond','foot']]
#plot:
plt.close('all')
fig,AX  = plt.subplots(2, 2, figsize=(8,6))
colors  = 'b', 'g', 'r'
for ax,c,f in zip(AX.flatten(), [0,0,1,1], [0,1,0,1] ):
	ind = (cond==c) & (foot==f)
	yy  = y[ind]
	for ii in range(3):
		for yyy in yy:
			ax.plot(yyy[:,ii], color=colors[ii])
plt.show()

