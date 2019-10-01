
'''
0D and 1D univariate and bivariate dataset class definitions

This module faciliates CI classes, mainly used for visualization.
Users should not instantiate these CI classes directly. Instead
use the bici.data module to create bivariate dataset objects, whose
methods can be used to calculate CIs, returning CI objects.
'''

from math import sqrt,pi,cos,sin,log
import numpy as np
from scipy import stats
from scipy.special import gamma
from matplotlib import pyplot as plt
import spm1d
from . ellipse import BivariateCI20D, BivariateConfidenceEllipse0D, BivariatePredictionEllipse0D
from . ellipse import BivariateCI21D, BivariateConfidenceEllipse1D, BivariatePredictionEllipse1D
from . interval import ConfidenceInterval0D,PredictionInterval0D
from . interval import ConfidenceInterval1D,PredictionInterval1D
from . plot import plot_multicolorline






class _Dataset(object):
	
	y = None    #data
	J = None    #sample size`
	
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
	def nobservations(self):
		return self.J
	@property
	def samplesize(self):
		return self.J

	def toarray(self):
		return self.y.copy()



class _Dataset1D(_Dataset):
	
	Q = None    #number of continuum nodes
	
	def _getx(self, x):
		return np.arange(self.Q) if (x is None) else x

	@property
	def nnodes(self):
		return self.Q
	



class UnivariateDataset0D(_Dataset):
	def __init__(self, y):
		self.y   = np.asarray(y)
		assert self.y.ndim==1, 'Data must be a list of scalars or a one-dimensional array'
		self.J   = self.y.shape[0]  #number of observations
		
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   sample size:  %d\n' %self.samplesize
		s += '   mean:         %s\n' %self.mean
		s += '   st.dev.:      %s\n' %self.std
		s += '   range:        %s\n' %str(self.range)
		return s
		
		
	def get_confidence_region(self, alpha=0.05):
		ci    = ConfidenceInterval0D(self, alpha)
		return ci

	def get_prediction_region(self, alpha=0.05):
		ci    = PredictionInterval0D(self, alpha)
		return ci

	def plot(self, ax=None, x=None, plot_sample_mean=True):
		ax  = self._gca(ax)
		x   = 0 if (x is None) else x
		ax.plot(x*np.ones(self.J), self.y, 'ko', label='Observations', mfc='0.3')
		if plot_sample_mean:
			ax.plot( x, self.mean, 'ko', label='Sample mean', ms=15, mfc='w')



class UnivariateDataset1D(_Dataset1D):
	def __init__(self, y):
		self.y   = np.asarray(y)
		assert self.y.ndim==2, 'Data must be a a two-dimensional array'
		self.J   = self.y.shape[0]  #number of observations
		self.Q   = self.y.shape[1]  #number of continuum nodes

	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   sample size:  %d\n' %self.samplesize
		s += '   nnodes:       %d\n' %self.nnodes
		return s

	def get_confidence_region(self, alpha=0.05):
		ci    = ConfidenceInterval1D(self, alpha)
		return ci

	def get_prediction_region(self, alpha=0.05):
		ci    = PredictionInterval1D(self, alpha)
		return ci

	def plot(self, ax=None, x=None, plot_sample_mean=True):
		ax  = self._gca(ax)
		x   = self._getx(x)
		h   = ax.plot(x, self.y.T, '-', color='0.7')
		if plot_sample_mean:
			plt.setp(h, lw=0.5)
			ax.plot( x, self.mean, 'k', lw=3, label='Sample mean')




class _BivariateDataset(_Dataset):
	
	_U = None  #svd (eigenvectors)
	_s = None  #svd (eigenvalues)
	_R = None  #svd (rotation matrix)
	I  = 2     #number of vector components (only I=2 supported)
	
	def _init_svd(self):
		U,s,R    = np.linalg.svd(self.cov)
		if np.dot(U[:,0], [0,1]) < 0:
			U   *= -1
			R   *= -1
		self._U  = U
		self._s  = s
		self._R  = R
		
	
	@property
	def Maxis(self):  #major axis unit vector
		return self._U[:,0]
	@property
	def maxis(self):  #minor axis unit vector
		return self._U[:,1]
	@property
	def ncomponents(self):
		return self.I

	def get_cov(self, bias=1):
		return np.cov(self.y.T, bias=bias)
	
	cov = property(get_cov)
	




class BivariateDataset0D(_BivariateDataset):
	
	def __init__(self, y):
		self.y   = np.asarray(y)
		assert self.y.ndim==2, 'Data must be a a two-dimensional array'
		self.J   = self.y.shape[0]  #number of observations
		self.I   = self.y.shape[1]  #number of components (I must equal 2)
		assert self.I==2, 'Only bivariate data (two vector components) supported. Number of components detected: %d' %self.I
		self._init_svd()
	
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   ncomponents:     %d\n' %self.I
		s += '   sample size:     %d\n' %self.J
		s += '   mean:            %s\n' %self.mean
		return s
	
	
	
	def get_ci2(self, alpha=0.05):
		return BivariateCI20D(self, alpha)

	def get_confidence_region(self, alpha=0.05):
		return BivariateConfidenceEllipse0D(self, alpha)

	def get_prediction_region(self, alpha=0.05):
		return BivariatePredictionEllipse0D(self, alpha)

	def plot(self, ax=None, plot_sample_mean=True, **kwdargs):
		ax  = self._gca(ax)
		x,y = self.y.T
		ax.plot(x, y, 'o', **kwdargs)
		if plot_sample_mean:
			x,y  = self.mean
			ax.plot( x, y, 'ko', ms=15, mfc='w', label='Sample mean')




class BivariateDataset1D(_BivariateDataset, _Dataset1D):
	
	def __init__(self, y):
		self.y   = np.asarray(y)
		assert self.y.ndim==3, 'Data must be a a three-dimensional array'
		self.J   = self.y.shape[0]  #number of observations
		self.Q   = self.y.shape[1]  #number of continuum nodes
		self.I   = self.y.shape[2]  #number of components
		assert self.I==2, 'Only bivariate data (two vector components) supported. Number of components detected: %d' %self.I
		self._init_svd()
		
		
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   sample size:     %d\n' %self.J
		s += '   nnodes:          %d\n' %self.Q
		s += '   ncomponents:     %d\n' %self.I
		return s
	
	def _init_svd(self):
		U,S,R     = [],[],[]
		W         = self.get_cov()
		for w in W:
			u,s,r = np.linalg.svd(w)
			if np.dot(u[:,0], [0,1]) < 0:
				u   *= -1
				r   *= -1
			U.append(u)
			S.append(s)
			R.append(r)
		self._U  = np.array(U)
		self._s  = np.array(S)
		self._R  = np.array(R)
		
	def get_ci2(self, alpha=0.05):
		return BivariateCI21D(self, alpha)

	def get_confidence_region(self, alpha=0.05):
		return BivariateConfidenceEllipse1D(self, alpha)

	def get_prediction_region(self, alpha=0.05):
		return BivariatePredictionEllipse1D(self, alpha)


	def get_cov(self, bias=1):
		W = np.array(  [np.cov(self.y[:,i,:].T, bias=bias)   for i in range(self.Q)]  )
		return W

	cov = property(get_cov)
	
	def get_frame(self, frame):
		return BivariateDataset0D(  self.y[:,frame,:]  )
		
		
	def plot(self, x=None, plot_sample_mean=True, lw=0.5):
		x    = self._getx(x)
		plt.figure(figsize=(8,3))
		ax0  = plt.axes([0.05, 0.10, 0.4, 0.8])
		ax1  = plt.axes([0.55, 0.10, 0.4, 0.8])
		ax0.plot( x, self.y[:,:,0].T, '0.7', lw=lw )
		ax1.plot( x, self.y[:,:,1].T, '0.7', lw=lw )
		ax0.plot( x, self.y[:,:,0].mean(axis=0), 'k', lw=3, label='Sample mean' )
		ax1.plot( x, self.y[:,:,1].mean(axis=0), 'k', lw=3 )
		ax0.set_title('Component 1')
		ax1.set_title('Component 2')
		ax0.legend()
		
	def plot_multicolorline(self, other):
		pass

	
