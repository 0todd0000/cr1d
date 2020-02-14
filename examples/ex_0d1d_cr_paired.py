
import numpy as np
from matplotlib import pyplot as plt
import cr1d



# Load data:
dataset = cr1d.data.FraminghamSystolicBloodPressure()
y0,y1   = dataset.y
print(dataset)
print('\n\n\n')


# Calculate confidence region:
cr      = cr1d.confidence_region_paired(y0, y1)
print(cr)




# Plot:
plt.close('all')
cr.plot()
plt.show()