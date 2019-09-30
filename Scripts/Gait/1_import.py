'''
Import raw ground reaction force (GRF) data from the Gait experiment.

50 trials of each of "NormalGait" and "FastGait"

Developed in Python 3.6

'''


import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt


def load_gait_csv(fname):
	A         = np.loadtxt(fname, delimiter=',', skiprows=1)
	y         = -A[:,2:]
	yR,yL     = y[:,:3], y[:,3:]
	return yR,yL
	

# #(0) Import single trial:  (development purposes)
# dir0        = Path( __file__ ).parents[2]   #main repository directory
# dirData     = os.path.join(dir0, 'Data', 'Gait', 'raw')
# fnameCSV    = os.path.join(dirData, 'NormalGait_01.csv')
# yR,yL       = load_gait_csv(fnameCSV)
# #plot:
# plt.close('all')
# fig,ax      = plt.subplots(1, 2, figsize=(8,3))
# ax[0].plot(yL)
# ax[1].plot(yR)
# plt.show()




#(1) Import all:
dir0        = Path( __file__ ).parents[2]                     # Main repository directory
dirRaw      = os.path.join(dir0, 'Data', 'Gait', 'Raw')       # Raw data directory
dirProc     = os.path.join(dir0, 'Data', 'Gait', 'Processed') # Processed data directory
cond_labels = ['NormalGait', 'FastGait'] # Condition labels
ntrials     = 50
COND        = []  # Condition (normal or fast walking)
FOOT        = []  # Foot (left=0, right=1)
Y           = []  # Dependent variable (1D ground reaction force)
for i,label in enumerate(cond_labels):
	for ii in range(ntrials):
		fname  = os.path.join( dirRaw , '%s_%02d.csv' %(label,ii+1) )
		yR,yL  = load_gait_csv(fname)
		Y     += [yR,yL]
		COND  += [i,i]
		FOOT  += [0,1]
y,cond,foot = [np.array(x) for x in [Y,COND,FOOT]]
fnameNPZ    = os.path.join(dirProc, '1_imported.npz')
np.savez_compressed(fnameNPZ, y=y, cond=cond, foot=foot, allow_pickle=True)


