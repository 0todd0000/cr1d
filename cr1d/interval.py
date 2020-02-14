'''
Probability intervals for 0D and 1D univariate data.

Users should not instantiate these interval classes directly. Instead
use the data module to create univariate dataset objects, whose
get* methods can be used to calculate and return probability
interval objects.
'''


from math import pi,atan2,degrees,cos,sin,log
import numpy as np
from scipy import stats
from scipy.special import gamma
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from spm1d import rft1d
from spm1d.stats import ttest2



class _Interval(object):
	
	def __init__(self, ds, alpha=None):
		self._ds    = ds
		self._gca   = ds._gca
		self.alpha  = 0.05 if alpha is None else alpha
		self.h      = None    #interval height
		self.x0     = None    #lower limit
		self.x1     = None    #upper limit
		self.set_alpha(alpha)
		

	@staticmethod
	def isinteger(x):
		return (x % 1) == 0
	
	@property
	def center(self):
		return self._ds.mean

	@property
	def height(self):
		return self.h

	@property
	def interval(self):
		return self.x0, self.x1

	@property
	def label_short(self):
		return self.pctstr + ' ' + self.region_type_short

	@property
	def pctstr(self):
		p = 100 * ( 1 - self.alpha )
		s = '%d'%p if self.isinteger(p) else str(p)
		return s + '%'

	def isinside(self, x):
		return np.logical_not(self.isoutside(x) )
	def isoutside(self, x):
		x0,x1    = self.interval
		return np.logical_or( (x<x0), (x>x1) )

	def ninside(self, x):
		return self.isinside(x).sum()
	def noutside(self, x):
		return self.isoutside(x).sum()

	def propinside(self, x):
		return self.isinside(x).mean()
	def propoutside(self, x):
		return self.isoutside(x).mean()


# class _MeanDifferenceInterval(_Interval):
# 	def __init__(self, ds0, ds1, alpha=None):
# 		self._ds0   = ds0
# 		self._ds1   = ds1
# 		self._gca   = ds0._gca
# 		self.alpha  = 0.05 if alpha is None else alpha
# 		self.h      = None    #interval height
# 		self.x0     = None    #lower limit
# 		self.x1     = None    #upper limit
# 		self.set_alpha(alpha)



class _Interval0D(_Interval):
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   alpha:       %.3f\n' %self.alpha
		s += '   height:      %s\n' %self.h
		s += '   interval:    [%s, %s]\n' %(self.x0, self.x1)
		s += '------------------\n'
		s += str(self._ds)
		return s


	def plot(self, ax=None, x=None, width=1, color=None):
		ax       = self._gca(ax)
		x        = 0 if (x is None) else x
		w,ww     = 0.5*width, 0.25 * width
		y0,y1    = self.interval
		h0       = ax.plot( [-w, w], [y0,y0], color=color, label=self.label_short)
		color    = h0[0].get_color()
		ax.plot( [-w, w], [y1,y1], color=color)
		verts    = [(-ww,y0), (ww,y0),    (ww,y1), (-ww,y1)]
		patches  = PatchCollection([Polygon(verts)])
		ax.add_collection(patches)
		plt.setp(patches, facecolor=color, alpha=0.5, linewidth=0)


class _Interval1D(_Interval):
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   alpha:       %.3f\n' %self.alpha
		s += '------------------\n'
		s += str(self._ds)
		return s


	def isinside(self, x):
		return not self.isoutside(x)
	def isoutside(self, x):
		return np.any(  super().isoutside(x)  )


	def plot(self, ax=None, x=None, **kwdargs):
		ax       = self._gca(ax)
		x        = self._ds._getx(x)
		ax.plot(x, self.x0, label=self.label_short, **kwdargs)
		ax.plot(x, self.x1, **kwdargs)
		





class ConfidenceInterval0D(_Interval0D):
	region_type       = 'confidence'
	region_type_short = 'CI'
	
	def _force_height(self, h):
		m       = self._ds.mean              #sample mean
		ci      = m-h, m+h                   #confidence interval
		self.h  = h                          #interval height
		self.x0 = ci[0]                      #lower limit
		self.x1 = ci[1]                      #upper limit
	
	def set_alpha(self, alpha=0.05):
		J       = self._ds.J                 #sample size
		m       = self._ds.mean              #sample mean
		s       = self._ds.std               #sample standard deviation
		c       = stats.t.isf(alpha/2, J-1)  #critical test statistic
		h       = c * s / J**0.5             #interval width
		ci      = m-h, m+h                   #confidence interval
		self.h  = h                          #interval height
		self.x0 = ci[0]                      #lower limit
		self.x1 = ci[1]                      #upper limit



class MeanDifferenceConfidenceInterval0D(_Interval0D):
	region_type       = 'confidence'
	region_type_short = 'CI'
	
	
	def __init__(self, ds0, ds1, alpha=None, equal_var=False):
		self._ds0   = ds0
		self._ds1   = ds1
		self._gca   = ds0._gca
		self.alpha  = 0.05 if alpha is None else alpha
		self.h      = None    #interval height
		self.x0     = None    #lower limit
		self.x1     = None    #upper limit
		self.set_alpha(ds1, alpha, equal_var)
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   alpha:       %.3f\n' %self.alpha
		s += '   height:      %s\n' %self.h
		s += '   interval:    [%s, %s]\n' %(self.x0, self.x1)
		s += '------------------\n'
		s += str(self._ds0)
		s += '------------------\n'
		s += str(self._ds1)
		return s
	
	
	def map_to_means(self, d0, d1):
		cr0   = ConfidenceInterval0D(d0, self.alpha)
		cr1   = ConfidenceInterval0D(d1, self.alpha)
		cr0._force_height(self.h/2)
		cr1._force_height(self.h/2)
		return cr0,cr1
	
	def set_alpha(self, other, alpha=0.05, equal_var=False):
		ds0,ds1 = self._ds0, self._ds1
		J0,J1   = ds0.J, ds1.J                # sample sizes
		m0,m1   = ds0.mean, ds1.mean          # sample means
		spmi    = ttest2(ds0.y, ds1.y, equal_var=equal_var).inference(alpha, two_tailed=True)
		s       = spmi.sigma2**0.5            # pooled standard deviation
		c       = spmi.zstar                  # critical test statistic
		h       = c * s * (1./J0 + 1./J1)**0.5
		m       = m0 - m1
		ci      = m-h, m+h                    # confidence interval
		self.h  = h                           # interval height
		self.x0 = ci[0]                       # lower limit
		self.x1 = ci[1]                       # upper limit


		
		
		
		# m0,m1   = ds0.mean, ds1.mean          # sample mean
		# s0,s1   = self._ds.std               #sample standard deviation
		# v       = J0 + J1 - 2                 # degrees of freedom
		# c       = stats.t.isf(alpha/2, v)     #critical test statistic
		# h       = c * s * (1./JA + 1./JB)**0.5


		# m1      = self._ds1.mean              #sample mean
		# 
		# c       = stats.t.isf(alpha/2, J-1)  #critical test statistic
		# h       = c * s / J**0.5             #interval width
		# ci      = m-h, m+h                   #confidence interval
		# self.h  = h                          #interval height
		# self.x0 = ci[0]                      #lower limit
		# self.x1 = ci[1]                      #upper limit


class PredictionInterval0D(_Interval0D):
	region_type       = 'prediction'
	region_type_short = 'PI'
	
	def set_alpha(self, alpha=0.05):
		J       = self._ds.J                 #sample size
		m       = self._ds.mean              #sample mean
		s       = self._ds.std               #sample standard deviation
		c       = stats.t.isf(alpha/2, J-1)  #critical test statistic
		h       = c * s * (1+(1/J))**0.5     #interval height
		ci      = m-h, m+h                   #confidence interval
		self.h  = h                          #interval height
		self.x0 = ci[0]                      #lower limit
		self.x1 = ci[1]                      #upper limit


class ConfidenceInterval1D(_Interval1D):
	region_type       = 'confidence'
	region_type_short = 'CI'
	
	def set_alpha(self, alpha=0.05):
		J       = self._ds.J                   #sample size
		Q       = self._ds.Q                   #numer of continuum nodes
		m       = self._ds.mean                #sample mean
		s       = self._ds.std                 #sample standard deviation
		r       = self._ds.y - m               #residuals
		efwhm   = rft1d.geom.estimate_fwhm(r)  #estimated smoothness
		c       = rft1d.t.isf(alpha/2, J-1, Q, efwhm)  #critical test statistic
		h       = c * s / J**0.5               #interval width
		ci      = m-h, m+h                     #confidence interval
		self.h  = h                            #interval height
		self.x0 = ci[0]                        #lower limit
		self.x1 = ci[1]                        #upper limit


class PredictionInterval1D(_Interval1D):
	region_type       = 'prediction'
	region_type_short = 'PI'
	
	def set_alpha(self, alpha=0.05):
		J       = self._ds.J                   #sample size
		Q       = self._ds.Q                   #numer of continuum nodes
		m       = self._ds.mean                #sample mean
		s       = self._ds.std                 #sample standard deviation
		r       = self._ds.y - m               #residuals
		efwhm   = rft1d.geom.estimate_fwhm(r)  #estimated smoothness
		c       = rft1d.t.isf(alpha/2, J-1, Q, efwhm)  #critical test statistic
		h       = c * s * (1+(1/J))**0.5       #interval height
		ci      = m-h, m+h                     #confidence interval
		self.h  = h                            #interval height
		self.x0 = ci[0]                        #lower limit
		self.x1 = ci[1]                        #upper limit
	
	
	
	
