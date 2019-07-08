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
from matplotlib import pyplot
from spm1d import rft1d
from matplotlib import pyplot
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection



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




class _Interval0D(_Interval):
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   alpha:       %.3f\n' %self.alpha
		s += '   height:      %s\n' %self.h
		s += '   interval:    [%s, %s]\n' %(self.x0, self.x1)
		s += '------------------\n'
		s += str(self._ds)
		return s


	def plot(self, ax=None, x=None, width=1, color='r'):
		ax       = self._gca(ax)
		x        = 0 if (x is None) else x
		w,ww     = 0.5*width, 0.25 * width
		y0,y1    = self.interval
		ax.plot( [-w, w], [y0,y0], color=color, label=self.label_short)
		ax.plot( [-w, w], [y1,y1], color=color)
		verts    = [(-ww,y0), (ww,y0),    (ww,y1), (-ww,y1)]
		patches  = PatchCollection([Polygon(verts)])
		ax.add_collection(patches)
		pyplot.setp(patches, facecolor=color, alpha=0.5, linewidth=0)


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
	
	
	
	
