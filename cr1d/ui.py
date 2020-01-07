'''
User interface

High-level functions for rapidly constructing statistical regions
'''


__all__ = ['cr', 'confidence_region']


import numpy as np
from . util import as_cr1d_dtype









def cr(y, alpha=0.05):
	d = as_cr1d_dtype(y)
	return d.get_confidence_region(alpha=alpha)

confidence_region = cr

