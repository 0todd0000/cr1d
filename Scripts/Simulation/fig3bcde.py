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
	ax.plot(J, fpr[:,:,i], 'o-', ms=3)
	ax.axhline(0.05, color='k', ls=':')
	plt.setp(ax, xlim=(4, 50), ylim=(-0.02, 1.15))
	if i==0:
		leg = ax.legend(['FWHM = %d%s' %(x,'%') for x in FWHM], loc='lower left', bbox_to_anchor=(0.5, 0.2))
		plt.setp( leg.get_texts() , size=8 )
[ax.set_xlabel('Sample size')  for ax in AX[1]]
[ax.set_ylabel('False positive rate')  for ax in AX[:,0]]
labels = ['RFT Confidence Region', 'RFT Prediction Region', 'CI2-mu', 'CI2-new']
[ax.text(0.5, 0.92, '(%s)  Bivariate 1D:  %s' %(chr(98+i),s), transform=ax.transAxes, ha='center', size=9)  for i,(ax,s) in enumerate(zip(AX.flatten(),labels))]
[ax.text(0.6, 0.08, r'$\alpha$ = 0.05', transform=ax.transAxes, ha='center', size=8)  for ax in AX.flatten()]	
plt.show()



# plt.savefig( os.path.join( os.path.dirname(__file__), 'figs', 'fig3bcde.pdf') )




