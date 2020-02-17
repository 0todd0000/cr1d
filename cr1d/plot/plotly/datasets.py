'''
plotly datasets
'''



import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d


# import plotly.graph_objects as go
#
# x,y,z = np.random.randn(50, 3).T
#
# s3d = go.Scatter3d(x=x, y=y, z=z, mode='markers')
#
# fig = go.Figure(data=[s3d])
# fig.show()




class DatasetPlotter(object):
	def __init__(self, ax):
		self.ax  = self._gca(ax)  # axes object
		
		
	@staticmethod
	def _gca(ax):
		if ax is None:
			ax = plt.gca()
		else:
			assert isinstance(ax, plt.Axes), 'ax must be None or a matplotlib axes object'
		return ax
	
	def _ensure3d(self):
		if not isinstance(self.ax, mplot3d.Axes3D):
			bbox    = self.ax.get_position()
			plt.delaxes(self.ax)
			self.ax = plt.axes(bbox, projection='3d')
		
		
	
	
	def scatter(self, *args, **kwdargs):
		return self.ax.scatter(*args, **kwdargs)
		#
		# x      = 0 if (x is None) else x
		# ax,J   = self.ax, self.d.J
		# h      = self.ax.scatter(x*np.ones(J), self.y, **kwdargs)
		# if plot_sample_mean:
		# 	fc = h.get_facecolor()[0][:3]
		# 	ec = h.get_edgecolor()[0][:3]
		# 	h1 = self.ax.plot( x, self.mean, 'o', ms=15, mfc=fc, mec=ec, alpha=0.5)[0]
		# 	return h,h1
		# else:
		# 	return h
		
	def scatter3d(self, *args, **kwdargs):
		self._ensure3d()
		return self.ax.scatter(*args, **kwdargs)






# def scatter_u0d(ds, ax=None, x=None, plot_sample_mean=True, **kwdargs):
# 	plotter = DatasetPlotter(ax)
# 	x       = 0 if (x is None) else x
# 	h       = self.ax.scatter(x*np.ones(ds.J), ds.y, **kwdargs)
# 	if plot_sample_mean:
# 		fc = h.get_facecolor()[0][:3]
# 		ec = h.get_edgecolor()[0][:3]
# 		h1 = self.ax.plot( x, self.mean, 'o', ms=15, mfc=fc, mec=ec, alpha=0.5)[0]
# 		return h,h1
# 	else:
# 		return h
#
#
# 	return plotter.scatter_u0d()
	