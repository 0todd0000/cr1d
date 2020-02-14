'''
User interface

High-level functions for rapidly constructing statistical regions
'''


__all__ = [
	'cr',
	'cr_onesample',
	'cr_paired',
	'cr_twosample',
	'confidence_region',
	'confidence_region_onesample',
	'confidence_region_paired',
	'confidence_region_twosample',
]


import numpy as np
from . util import as_cr1d_dtype






def cr(y, alpha=0.05):
	d = as_cr1d_dtype(y)
	return d.get_confidence_region(alpha=alpha)

def cr_paired(y0, y1, alpha=0.05):
	d = as_cr1d_dtype(y0-y1)
	return d.get_confidence_region(alpha=alpha)

def cr_twosample(y0, y1, alpha=0.05, equal_var=False):
	d0 = as_cr1d_dtype(y0)
	d1 = as_cr1d_dtype(y1)
	return d0.get_twosample_confidence_region(d1, alpha=alpha, equal_var=equal_var)



cr_onesample                = cr
confidence_region           = cr
confidence_region_onesample = cr
confidence_region_paired    = cr_paired
confidence_region_twosample = cr_twosample

