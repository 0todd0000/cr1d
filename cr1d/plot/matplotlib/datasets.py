'''
matplotlib datasets
'''


import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d




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
		
		
	def plot(self, *args, **kwdargs):
		return self.ax.plot(*args, **kwdargs)

	def plot_bivariate1d(self, y, **kwdargs):
		h0  = self.ax.plot( y[0,:,0] )[0]
		h1  = self.ax.plot( y[0,:,1] )[0]
		c0  = h0.get_color()
		c1  = h1.get_color()
		hh0 = self.ax.plot( y[1:,:,0].T , color=c0 )
		hh1 = self.ax.plot( y[1:,:,1].T , color=c1 )

	def plot_trivariate1d(self, y, **kwdargs):
		h0  = self.ax.plot( y[0,:,0] )[0]
		h1  = self.ax.plot( y[0,:,1] )[0]
		h2  = self.ax.plot( y[0,:,2] )[0]
		c0  = h0.get_color()
		c1  = h1.get_color()
		c2  = h2.get_color()
		hh0 = self.ax.plot( y[1:,:,0].T , color=c0 )
		hh1 = self.ax.plot( y[1:,:,1].T , color=c1 )
		hh2 = self.ax.plot( y[1:,:,2].T , color=c2 )

	
	
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
	