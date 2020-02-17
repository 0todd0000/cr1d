
'''
0D and 1D univariate and bivariate dataset class definitions

This module faciliates CI classes, mainly used for visualization.
Users should not instantiate these CI classes directly. Instead
use the bici.data module to create bivariate dataset objects, whose
methods can be used to calculate CIs, returning CI objects.
'''

__all__ = ['Univariate0D', 'Bivariate0D', 'Trivariate0D',   'Univariate1D', 'Bivariate1D', 'Trivariate1D']


from math import sqrt,pi,cos,sin,log
import numpy as np
from scipy import stats
from scipy.special import gamma
from matplotlib import pyplot as plt
import spm1d
from . ellipse import BivariateConfidenceEllipse0D, BivariatePredictionEllipse0D
from . ellipse import BivariateConfidenceEllipse1D, BivariatePredictionEllipse1D
from . interval import ConfidenceInterval0D,PredictionInterval0D
from . interval import MeanDifferenceConfidenceInterval0D
from . interval import ConfidenceInterval1D,PredictionInterval1D
from . plot import plot_ci2style, plot_multicolorline




def as_cr1d_dtype(y):
	y = np.asarray(y)
	if y.ndim == 1:
		d     = Univariate0D(y)
	elif y.ndim == 2:
		m,n = y.shape
		if n==2:
			d = Bivariate0D(y)
		elif n==3:
			d = Trivariate0D(y)
		else:
			d = Univariate1D(y)
	elif y.ndim == 3:
		J,Q,I = y.shape
		if I==2:
			d = Bivariate1D(y)
		elif I==3:
			d = Trivariate1D(y)
		else:
			raise ValueError( f'For 3-dimensional arrays with shape (n0,n1,n2): n2 must be 2 or 3. Detected n2 = {I}')
	else:
		raise ValueError( f'Array must be 1, 2 or 3 dimensional. Number of dimensions detected: {y.ndim}')
	return d



def Dataset(y):
	return as_cr1d_dtype(y)



class _Dataset(object):
	
	_dim  = 1       # required array dimension
	_I    = None    # required number of vector components
	_minJ = 3       # minimum number of observations supported in cr1d
	_minQ = None    # minimum number of domain nodes supported in cr1d
	y     = None    # data
	dim   = 0       # domain dimensionality
	J     = None    # sample size
	Q     = None    # number of measurement domain nodes
	I     = None    # number of vector components
	
	def __init__(self, y):
		self.y   = np.asarray(y)
		self._init()


	@staticmethod
	def _gca(ax):
		if ax is None:
			ax = plt.gca()
		else:
			assert isinstance(ax, plt.Axes), 'ax must be None or a matplotlib axes object'
		return ax

	@property
	def mean(self):
		return self.y.mean(axis=0)
	@property
	def range(self):
		return self.y.min(axis=0), self.y.max(axis=0)
	@property
	def std(self):
		return self.y.std(axis=0, ddof=1)
	@property
	def ncomponents(self):
		return self.I
	@property
	def ndim(self):
		return self.y.ndim
	@property
	def nobservations(self):
		return self.J
	@property
	def nnodes(self):
		return self.Q
	@property
	def sample_size(self):
		return self.J
	@property
	def shape(self):
		return self.y.shape

	def _assert_array(self):
		pass
	
	
	def _assert_dim(self):
		assert self.y.ndim==self._dim, f'"y" must be a {self._dim}-dimensional array'
		
	def _assert_I(self, I):
		assert I==self._I, f'The second dimension of "y" must be {self._I}.  Dimensionality detected: {I}'
	def _assert_J(self, J):
		assert J>=self._minJ, f'There must be at least {self._minJ} observations (i.e., the first dimension of "y" must be at least {self._minJ}).  Number of observations detected: {J}'
	def _assert_Q(self, Q):
		assert Q>=self._minQ, f'There must be at least {self._minQ} domain nodes (i.e., the second dimension of "y" must be at least {self._minQ}).  Number of nodes detected: {Q}'

	def _assert_no_nan(self):
		pass
	
	def _assert_numeric(self):
		pass
		
	def _assert_zero_variance(self):
		pass
	
	
	
	
	def _init(self):
		# assert dimensionality:
		self._assert_array()
		self._assert_dim()
		self._assert_numeric()
		self._assert_no_nan()
		self._assert_zero_variance()
		
		# assert number of observations
		self._assert_J( self.y.shape[0] )
		
		# assert number of vector components
		if self._I is not None:
			if self.ndim==2:
				self._assert_I( self.y.shape[1] )
			else:
				self._assert_I( self.y.shape[2] )

		# assert number of domain nodes
		if self._minQ is not None:
			self._assert_Q( self.y.shape[1] )


	
	
	
	def toarray(self):
		return self.y.copy()



class _Dataset1D(_Dataset):
	
	_minQ = 10    # minimum number of domain nodes supported in cr1d
	dim   = 1     # domain dimensionality

	def _getx(self, x):
		return np.arange(self.Q) if (x is None) else x






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

	def plot(self, ax=None, x=None, plot_sample_mean=True):
		ax  = self._gca(ax)
		x   = 0 if (x is None) else x
		ax.plot(x*np.ones(self.J), self.y, 'ko', label='Observations', mfc='0.3')
		if plot_sample_mean:
			ax.plot( x, self.mean, 'ko', label='Sample mean', ms=15, mfc='w')



class Bivariate0D(_Dataset):
	
	_dim = 2
	_I   = 2




class Trivariate0D(_Dataset):
	
	_dim = 2
	_I   = 3
	





class Univariate1D(_Dataset1D):

	_dim = 2
	


class Bivariate1D(_Dataset1D):
	
	_dim = 3
	_I   = 2
	

	
class Trivariate1D(_Dataset1D):
	
	_dim = 3
	_I   = 3
	







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
# class _BivariateDataset(_Dataset):
#
# 	_U = None  #svd (eigenvectors)
# 	_s = None  #svd (eigenvalues)
# 	_R = None  #svd (rotation matrix)
# 	I  = 2     #number of vector components (only I=2 supported)
#
# 	def _init_svd(self):
# 		U,s,R    = np.linalg.svd(self.cov)
# 		if np.dot(U[:,0], [0,1]) < 0:
# 			U   *= -1
# 			R   *= -1
# 		self._U  = U
# 		self._s  = s
# 		self._R  = R
#
#
# 	@property
# 	def Maxis(self):  #major axis unit vector
# 		return self._U[:,0]
# 	@property
# 	def maxis(self):  #minor axis unit vector
# 		return self._U[:,1]
# 	@property
# 	def ncomponents(self):
# 		return self.I
#
# 	def get_cov(self, bias=1):
# 		return np.cov(self.y.T, bias=bias)
#
# 	cov = property(get_cov)
#
#
#
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


	
