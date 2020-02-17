
import numpy as np
from matplotlib import pyplot as plt
import cr1d
cr1d.set_color_cycle()




# isinstance(ax, mplot3d.Axes3D)

# from mpl_toolkits import mplot3d
#
# fig,ax = plt.subplots(2, 3, figsize=(10,6))
#
# # fig = plt.figure()
# # ax = fig.gca(projection='3d')
# #
# # type(ax) =
#
# axx = ax[0,2]
# bbox = axx.get_position()
#
#
# plt.delaxes(ax[0,2])
# # ax = plt.subplot(2, 3, 3, projection='3d')
# # (x,y),(w,h)
#
#
#
# ax = plt.axes(bbox, projection='3d')
#
#
#
#
#
# plt.show()
#
#




np.random.seed(0)


# Univariate 0D:
y0      = np.random.randn(8)
d0      = cr1d.Dataset(y0)

# Bivariate 0D:
y1      = np.random.randn(12,2)
d1      = cr1d.Dataset(y1)


# Trivariate 0D:
y2      = np.random.randn(12,3)
d2      = cr1d.Dataset(y2)


# Univariate 1D:
y3      = np.random.randn(8, 101)
d3      = cr1d.Dataset(y3)

# Bivariate 1D:
y4      = np.random.randn(8,101,2)
y4[:,:,1] += 3
d4      = cr1d.Dataset(y4)


# Trivariate 1D:
y5      = np.random.randn(5,101,3)
y5[:,:,1] += 3
y5[:,:,2] += 6
d5      = cr1d.Dataset(y5)









# Plot:
plt.close('all')
fig,ax  = plt.subplots(2, 3, figsize=(12,6))
h0,h1   = d0.plot(ax=ax[0,0])
d1.plot(ax=ax[0,1])
d2.plot(ax=ax[0,2])
d3.plot(ax=ax[1,0])
d4.plot(ax=ax[1,1])
d5.plot(ax=ax[1,2])

plt.show()





