
import numpy as np
from matplotlib import pyplot as plt
import cr1d



# Load data:
dataset = cr1d.data.MinnesotaGeyerRate()
dataset = cr1d.data.WebsterSleep()
y       = dataset.y
print(dataset)
print('\n\n\n')


# Calculate confidence region:
cr      = cr1d.confidence_region(y)
print(cr)


# Plot:
plt.close('all')
cr.plot()
plt.show()