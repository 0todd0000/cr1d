'''
Create Fig.3a from the main manuscript.
'''

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt



#(0) Load simulation results:
dir0        = Path( __file__ ).parents[2] # Main repository directory
fnameNPZ    = os.path.join(dir0, 'Data', 'Simulation', 'results1d.npz')   # Simulation results file name
with np.load(fnameNPZ) as Z:
	J,FWHM,fpr = Z['J'], Z['FWHM'], Z['fpr']



#(1) Plot:
plt.close('all')
fig,AX = plt.subplots(2, 2, figsize=(8,6) )
for i,ax in enumerate( AX.flatten() ):
	ax.plot(J, fpr[:,:,i])
	ax.legend(['FWHM = %d%s' %(x,'%') for x in FWHM])
	ax.axhline(0.05, color='k', ls=':')
plt.show()








