'''
User interface

High-level functions for rapidly constructing statistical regions
'''

__all__ = ['as_cr1d_dtype']


import numpy as np
from . dtypes import *





def as_cr1d_dtype(y):
	y = np.asarray(y)
	if y.ndim ==1:
		d= Univariate0D(y)
	return d
	



