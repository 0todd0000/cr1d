'''
Import raw center of pressure (COP) data from the Posture experiment.

10 trials of each of "Quiet" and "OneLeg"

Developed in Python 3.6
'''


import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt


def load_posture_csv(fname):
	A         = np.loadtxt(fname, delimiter=',', skiprows=1)
	return A[:,2:]
	

# #(0) Import single trial:  (development purposes)
# dir0        = Path( __file__ ).parents[2]   #main repository directory
# dirData     = os.path.join(dir0, 'Data', 'Posture', 'Raw')
# fnameCSV    = os.path.join(dirData, 'Quiet_01.csv')
# cop         = load_posture_csv(fnameCSV)
# #plot:
# plt.close('all')
# fig,ax      = plt.subplots(1, 1, figsize=(6,6))
# ax.plot(cop[:,0], cop[:,1], '.')
# ax.axis('equal')
# plt.show()




#(1) Import all:
dir0        = Path( __file__ ).parents[2]                     # Main repository directory
dirRaw      = os.path.join(dir0, 'Data', 'Posture', 'Raw')       # Raw data directory
dirProc     = os.path.join(dir0, 'Data', 'Posture', 'Processed') # Processed data directory
cond_labels = ['Quiet', 'OneLeg'] # Condition labels
ntrials     = 10
COND        = []  # Condition (quiet or one-leg)
Y           = []  # Dependent variable (1D ground reaction force)
for i,label in enumerate(cond_labels):
	for ii in range(ntrials):
		fname  = os.path.join( dirRaw , '%s_%02d.csv' %(label,ii+1) )
		cop    = load_posture_csv(fname)
		Y.append( cop )
		COND.append(i)
y,cond      = [np.array(x) for x in [Y,COND]]
fnameNPZ    = os.path.join(dirProc, '1_imported.npz')
np.savez_compressed(fnameNPZ, y=y, cond=cond, allow_pickle=True)

