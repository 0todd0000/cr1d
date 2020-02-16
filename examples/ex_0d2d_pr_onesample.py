
import numpy as np
from matplotlib import pyplot as plt
import cr1d



# Load data:
dataset = cr1d.data.Iris()
y       = dataset.y
# y0,y1   = dataset.y
print(dataset)
print('\n\n\n')


# d = cr1d.util.as_cr1d_dtype(y)




# # Calculate confidence region:
# pr      = cr1d.prediction_region(y)
# print(pr)





#
#
# # Check that (a) and (b) are equal, where:
# #  (a) = distance between zero and the difference CR
# #  (b) = distance between the sample CRs
# print( dcr.interval[0] )
# print( cr0.interval[0] - cr1.interval[1] )
#
#
# # Plot:
# plt.close('all')
# fig,ax = plt.subplots(1, 2, figsize=(4,4))
# dcr.plot(ax[0])
# cr0.plot(ax[1])
# cr1.plot(ax[1])
# ax[0].set_title('Difference CR')
# ax[1].set_title('Sample CRs')
# plt.setp(ax, ylim=(-0.5,6.5))
# [axx.axhline(0, ls='--', color='k') for axx in ax]
# plt.show()



