
'''
0D and 1D univariate and bivariate dataset class definitions

This module faciliates CI classes, mainly used for visualization.
Users should not instantiate these CI classes directly. Instead
use the bici.data module to create bivariate dataset objects, whose
methods can be used to calculate CIs, returning CI objects.
'''

# __all__ = ['Univariate0D', 'Bivariate0D', 'Trivariate0D',   'Univariate1D', 'Bivariate1D', 'Trivariate1D']


from math import sqrt,pi,cos,sin,log
import numpy as np
from scipy import stats
from scipy.special import gamma
import spm1d
# from .. ellipse import BivariateConfidenceEllipse0D, BivariatePredictionEllipse0D
# from .. ellipse import BivariateConfidenceEllipse1D, BivariatePredictionEllipse1D
# from .. interval import ConfidenceInterval0D,PredictionInterval0D
# from .. interval import MeanDifferenceConfidenceInterval0D
# from .. interval import ConfidenceInterval1D,PredictionInterval1D
# from .. plot import plot_ci2style, plot_multicolorline








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
		self.I = I
	def _assert_J(self, J):
		assert J>=self._minJ, f'There must be at least {self._minJ} observations (i.e., the first dimension of "y" must be at least {self._minJ}).  Number of observations detected: {J}'
		self.J = J
	def _assert_Q(self, Q):
		assert Q>=self._minQ, f'There must be at least {self._minQ} domain nodes (i.e., the second dimension of "y" must be at least {self._minQ}).  Number of nodes detected: {Q}'
		self.Q = Q

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










