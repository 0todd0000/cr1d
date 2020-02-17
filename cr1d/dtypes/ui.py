
import numpy as np
from . dtypes0d import Univariate0D, Bivariate0D, Trivariate0D
from . dtypes1d import Univariate1D, Bivariate1D, Trivariate1D




def _as_cr1d_dtype(y):
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
	return _as_cr1d_dtype(y)