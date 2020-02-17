'''
plotly datasets
'''


import numpy as np
import plotly.graph_objects as go
# from plotly.subplots import make_subplots




class DatasetPlotter(object):
	def __init__(self, fig):
		self.fig  = fig  # figure object
		
		
	# @staticmethod
	# def _gca(ax):
	# 	if ax is None:
	# 		ax = plt.gca()
	# 	else:
	# 		assert isinstance(ax, plt.Axes), 'ax must be None or a matplotlib axes object'
	# 	return ax
	#
	# def _ensure3d(self):
	# 	if not isinstance(self.ax, mplot3d.Axes3D):
	# 		bbox    = self.ax.get_position()
	# 		plt.delaxes(self.ax)
	# 		self.ax = plt.axes(bbox, projection='3d')
		
		
	
	
	def scatter(self, x, y, **kwdargs):
		
		
		trace   = go.Scatter(x=x, y=y, mode='markers')
		row,col = None, None
		if 'row' in kwdargs.keys():
			row,col = kwdargs['row'], kwdargs['col']
		self.fig.add_trace( trace , row=row, col=col )
		

		
		
		# h      = self.ax.scatter(x*np.ones(J), self.y, **kwdargs)
		# if plot_sample_mean:
		# 	fc = h.get_facecolor()[0][:3]
		# 	ec = h.get_edgecolor()[0][:3]
		# 	h1 = self.ax.plot( x, self.mean, 'o', ms=15, mfc=fc, mec=ec, alpha=0.5)[0]
		# 	return h,h1
		# else:
		# 	return h
		
	def scatter3d(self, x, y, z, **kwdargs):
		trace = go.Scatter3d(x=x, y=y, z=z, mode='markers')
		row,col = None, None
		if 'row' in kwdargs.keys():
			row,col = kwdargs['row'], kwdargs['col']
		self.fig.add_trace( trace , row=row, col=col )
		
		
		# return self.ax.scatter(*args, **kwdargs)






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
	