'''
Create Fig.3a from the main manuscript.
'''

import os
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt



#(0) Load simulation results:
dir0        = Path( __file__ ).parents[2] # Main repository directory
fnameNPZ    = os.path.join(dir0, 'Data', 'Simulation', 'results0d.npz')   # Simulation results file name
with np.load(fnameNPZ) as Z:
	J,fpr   = Z['J'], Z['fpr']



#(1) Plot:
plt.close('all')
plt.figure( figsize=(6,4) )
ax = plt.axes()
ax.plot(J, fpr)
ax.legend(['CR', 'PR', 'CI2-mu', 'CI2-new'])
ax.axhline(0.05, color='k', ls=':')
ax.set_xlabel('Sample size')
ax.set_ylabel('False positive rate')
plt.show()



# plt.savefig( os.path.join( os.path.dirname(__file__), 'figs', 'fig3a.pdf') )



