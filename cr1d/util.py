'''
User interface

High-level functions for rapidly constructing statistical regions
'''

__all__ = ['as_cr1d_data']


import numpy as np
from . dtypes import *





def as_cr1d_data(y):
	y = np.asarray(y)
	if y.ndim ==1:
		d= Univariate0D(y)
	return d
	



