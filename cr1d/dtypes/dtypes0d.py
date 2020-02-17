
import numpy as np
from .. ellipse import BivariateConfidenceEllipse0D, BivariatePredictionEllipse0D
from .. interval import ConfidenceInterval0D,PredictionInterval0D
from .. interval import MeanDifferenceConfidenceInterval0D
# from .. plot import plot_ci2style, plot_multicolorline
from . _base import _Dataset
from .. plot import DatasetPlotter





class Univariate0D(_Dataset):
	
	_dim = 1

	
	def __repr__(self):
		s  = 'CR1D Data (%s)\n' %self.__class__.__name__
		s += '   sample size:  %d\n' %self.sample_size
		s += '   mean:         %s\n' %self.mean
		s += '   std:          %s\n' %self.std
		s += '   range:        %s\n' %str(self.range)
		return s
		
		
	def get_confidence_region(self, alpha=0.05):
		return ConfidenceInterval0D(self, alpha)

	
	def get_twosample_confidence_region(self, other, alpha=0.05, equal_var=False):
		dcr = MeanDifferenceConfidenceInterval0D(self, other, alpha, equal_var)
		cr0,cr1 = dcr.map_to_means(self, other)
		return dcr,cr0,cr1
	
	def get_prediction_region(self, alpha=0.05):
		return PredictionInterval0D(self, alpha)

	def plot(self, ax=None, x=None, plot_sample_mean=True, **kwdargs):
		plotter = DatasetPlotter(ax)
		x       = 0 if (x is None) else x
		h0      = plotter.scatter(x*np.ones(self.J), self.y, **kwdargs)
		# h1      = None
		# if plot_sample_mean:
		# 	fc  = h0.get_facecolor()[0][:3]
		# 	ec  = h0.get_edgecolor()[0][:3]
		# 	h1  = plotter.scatter( [x], [self.mean], s=200, fc=fc, ec=ec, alpha=0.5)
		# return h0,h1
		



class Bivariate0D(_Dataset):
	
	_dim = 2
	_I   = 2


	def plot(self, ax=None, plot_sample_mean=True, **kwdargs):
		plotter = DatasetPlotter(ax)
		y0,y1   = self.y.T
		h0      = plotter.scatter(y0, y1, **kwdargs)
		# h1      = None
		# if plot_sample_mean:
		# 	fc  = h0.get_facecolor()[0][:3]
		# 	ec  = h0.get_edgecolor()[0][:3]
		# 	h1  = plotter.scatter( *self.mean, s=200, fc=fc, ec=ec, alpha=0.5)
		# return h0,h1




class Trivariate0D(_Dataset):
	
	_dim = 2
	_I   = 3
	

	def plot(self, ax=None, plot_sample_mean=True, **kwdargs):
		plotter  = DatasetPlotter(ax)
		# y0,y1,y2 = self.y.T
		plotter.scatter3d(*self.y.T)
		# ax    = self._gca(ax)
		
		
		
		
		
		# ax = fig.gca(projection='3d')
		#
		# projection='3d'
		#
		# #(0) Generate coordinates:
		# np.random.seed(0)
		# x,y,z  = np.random.randn(10,3).T


		# #(1) Plot:
		# plt.close('all')
		# fig = plt.figure()
		# ax = mplot3d.Axes3D(fig)
		# ax.plot(x, y, z, 'o')
		# plt.show()



#
#
# class BivariateDataset0D(_BivariateDataset):
#
# 	def __init__(self, y):
# 		self.y   = np.asarray(y)
# 		assert self.y.ndim==2, 'Data must be a a two-dimensional array'
# 		self.J   = self.y.shape[0]  #number of observations
# 		self.I   = self.y.shape[1]  #number of components (I must equal 2)
# 		assert self.I==2, 'Only bivariate data (two vector components) supported. Number of components detected: %d' %self.I
# 		self._init_svd()
#
#
# 	def __repr__(self):
# 		s  = '%s\n' %self.__class__.__name__
# 		s += '   ncomponents:     %d\n' %self.I
# 		s += '   sample size:     %d\n' %self.J
# 		s += '   mean:            %s\n' %self.mean
# 		return s
#
#
#
# 	def get_ci2(self, alpha=0.05):
# 		return BivariateCI20D(self, alpha)
#
# 	def get_confidence_region(self, alpha=0.05):
# 		return BivariateConfidenceEllipse0D(self, alpha)
#
# 	def get_prediction_region(self, alpha=0.05):
# 		return BivariatePredictionEllipse0D(self, alpha)
#
# 	def plot(self, ax=None, plot_sample_mean=True, **kwdargs):
# 		ax  = self._gca(ax)
# 		x,y = self.y.T
# 		h   = ax.plot(x, y, 'o', **kwdargs)[0]
# 		if plot_sample_mean:
# 			x,y  = self.mean
# 			hh   = ax.plot( x, y, 'ko', ms=15, mfc='w', label='Sample mean')[0]
# 			h    = [h,hh]
# 		return h
#
#
