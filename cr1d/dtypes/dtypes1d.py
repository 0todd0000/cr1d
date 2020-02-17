
import numpy as np
# from .. ellipse import BivariateConfidenceEllipse1D, BivariatePredictionEllipse1D
# from .. interval import ConfidenceInterval1D,PredictionInterval1D
# from .. plot import plot_ci2style, plot_multicolorline
from . _base import _Dataset1D

from .. plot import DatasetPlotter



class Univariate1D(_Dataset1D):

	_dim = 2
	
	def plot(self, ax=None, plot_sample_mean=True, **kwdargs):
		plotter = DatasetPlotter(ax)
		h0      = plotter.plot(self.y.T, **kwdargs)
		# h1      = None
		# if plot_sample_mean:
		# 	fc  = h0.get_facecolor()[0][:3]
		# 	ec  = h0.get_edgecolor()[0][:3]
		# 	h1  = plotter.scatter( [x], [self.mean], s=200, fc=fc, ec=ec, alpha=0.5)
		# return h0,h1
	
	
	


class Bivariate1D(_Dataset1D):
	
	_dim = 3
	_I   = 2
	
	def plot(self, ax=None, plot_sample_mean=True, **kwdargs):
		plotter = DatasetPlotter(ax)
		h0      = plotter.plot_bivariate1d(self.y, **kwdargs)
	

	
class Trivariate1D(_Dataset1D):
	
	_dim = 3
	_I   = 3
	
	def plot(self, ax=None, plot_sample_mean=True, **kwdargs):
		plotter = DatasetPlotter(ax)
		h0      = plotter.plot_trivariate1d(self.y, **kwdargs)
	






# class UnivariateDataset1D(_Dataset1D):
# 	def __init__(self, y):
# 		self.y   = np.asarray(y)
# 		assert self.y.ndim==2, 'Data must be a a two-dimensional array'
# 		self.J   = self.y.shape[0]  #number of observations
# 		self.Q   = self.y.shape[1]  #number of continuum nodes
#
# 	def __repr__(self):
# 		s  = '%s\n' %self.__class__.__name__
# 		s += '   sample size:  %d\n' %self.samplesize
# 		s += '   nnodes:       %d\n' %self.nnodes
# 		return s
#
# 	def get_confidence_region(self, alpha=0.05):
# 		ci    = ConfidenceInterval1D(self, alpha)
# 		return ci
#
# 	def get_prediction_region(self, alpha=0.05):
# 		ci    = PredictionInterval1D(self, alpha)
# 		return ci
#
# 	def plot(self, ax=None, x=None, plot_sample_mean=True):
# 		ax  = self._gca(ax)
# 		x   = self._getx(x)
# 		h   = ax.plot(x, self.y.T, '-', color='0.7')
# 		if plot_sample_mean:
# 			plt.setp(h, lw=0.5)
# 			ax.plot( x, self.mean, 'k', lw=3, label='Sample mean')
#
#
#
#







#
#
# class BivariateDataset1D(_BivariateDataset, _Dataset1D):
#
# 	def __init__(self, y):
# 		self.y   = np.asarray(y)
# 		assert self.y.ndim==3, 'Data must be a a three-dimensional array'
# 		self.J   = self.y.shape[0]  #number of observations
# 		self.Q   = self.y.shape[1]  #number of continuum nodes
# 		self.I   = self.y.shape[2]  #number of components
# 		assert self.I==2, 'Only bivariate data (two vector components) supported. Number of components detected: %d' %self.I
# 		self._init_svd()
#
#
#
# 	def __repr__(self):
# 		s  = '%s\n' %self.__class__.__name__
# 		s += '   sample size:     %d\n' %self.J
# 		s += '   nnodes:          %d\n' %self.Q
# 		s += '   ncomponents:     %d\n' %self.I
# 		return s
#
# 	def _init_svd(self):
# 		U,S,R     = [],[],[]
# 		W         = self.get_cov()
# 		for w in W:
# 			u,s,r = np.linalg.svd(w)
# 			if np.dot(u[:,0], [0,1]) < 0:
# 				u   *= -1
# 				r   *= -1
# 			U.append(u)
# 			S.append(s)
# 			R.append(r)
# 		self._U  = np.array(U)
# 		self._s  = np.array(S)
# 		self._R  = np.array(R)
#
# 	def get_ci2(self, alpha=0.05):
# 		return BivariateCI21D(self, alpha)
#
# 	def get_confidence_region(self, alpha=0.05):
# 		return BivariateConfidenceEllipse1D(self, alpha)
#
# 	def get_prediction_region(self, alpha=0.05):
# 		return BivariatePredictionEllipse1D(self, alpha)
#
#
# 	def get_cov(self, bias=1):
# 		W = np.array(  [np.cov(self.y[:,i,:].T, bias=bias)   for i in range(self.Q)]  )
# 		return W
#
# 	cov = property(get_cov)
#
# 	def get_frame(self, frame):
# 		return BivariateDataset0D(  self.y[:,frame,:]  )
#
#
# 	def plot(self, x=None, plot_sample_mean=True, lw=0.5):
# 		x    = self._getx(x)
# 		plt.figure(figsize=(8,3))
# 		ax0  = plt.axes([0.05, 0.10, 0.4, 0.8])
# 		ax1  = plt.axes([0.55, 0.10, 0.4, 0.8])
# 		ax0.plot( x, self.y[:,:,0].T, '0.7', lw=lw )
# 		ax1.plot( x, self.y[:,:,1].T, '0.7', lw=lw )
# 		ax0.plot( x, self.y[:,:,0].mean(axis=0), 'k', lw=3, label='Sample mean' )
# 		ax1.plot( x, self.y[:,:,1].mean(axis=0), 'k', lw=3 )
# 		ax0.set_title('Component 1')
# 		ax1.set_title('Component 2')
# 		ax0.legend()
#
# 	def plot_ci2style(self, ax, other, z=None, cmap='jet', alpha=0.5, w=0.1, ec=None, ew=1, vmin=None, vmax=None, th=None):
# 		self.plot_multicolorline(ax, z=z, cmap=cmap, alpha=alpha, w=w, ec=ec, ew=ew, vmin=vmin, vmax=vmax, th=th)
# 		other.plot_multicolorline(ax, z=z, cmap=cmap, alpha=alpha, w=w, ec=ec, ew=ew, vmin=vmin, vmax=vmax, th=th)
#
#
#
# 	def plot_multicolorline(self, ax, z=None, cmap='jet', alpha=0.5, w=0.1, ec=None, ew=1, vmin=None, vmax=None, th=None):
# 		x,y = self.y.mean(axis=0).T
# 		plot_multicolorline(ax, x, y, z, cmap=cmap, alpha=alpha, w=w, ec=ec, vmin=vmin, vmax=vmax, th=th)
#


	
#