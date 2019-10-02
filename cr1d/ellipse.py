'''
Probability ellipses for 0D and 1D bivariate data.

Users should not instantiate these ellipse classes directly. Instead
use the data module to create bivariate dataset objects, whose
get* methods can be used to calculate and return probability
ellipse objects.
'''


from math import pi,atan2,degrees,cos,sin,log
import numpy as np
from scipy import stats
from scipy.special import gamma
from matplotlib import pyplot as plt
from matplotlib import patches
from spm1d import rft1d





class _Ellipse(object):
	
	def __init__(self, ds, alpha=None):
		self._ds    = ds
		self.alpha  = 0.05 if alpha is None else alpha
		self.L0     = None
		self.L1     = None
		self.set_alpha(alpha)
		
	@staticmethod
	def isinteger(x):
		return (x % 1) == 0
	
	@property
	def Maxis(self):  #major axis unit vector
		return self._ds.Maxis
	@property
	def maxis(self):  #minor axis unit vector
		return self._ds.maxis

	@property
	def area(self):
		return pi * self.L0 * self.L1
	
	@property
	def centroid(self):
		return self._ds.mean

	@property
	def eccentricity(self):
		return self.L0/self.L1
	
	@property
	def label_short(self):
		return self.pctstr + ' ' + self.region_type_short
	
	@property
	def orientation(self):
		return self.theta

	@property
	def pctstr(self):
		p = 100 * ( 1 - self.alpha )
		s = '%d'%p if self.isinteger(p) else str(p)
		return s + '%'

	@property
	def semi_axis_lengths(self):
		return np.array([self.L0, self.L1])

	@property
	def theta(self):
		x,y = self.Maxis
		return atan2(y, x)
	
	@property
	def thetad(self):
		return degrees(self.theta)
	

	
	def ispointinside(self, r):
		return np.logical_not(self.ispointoutside(r) )

	def ispointoutside(self, r):
		return self.isoutside(np.array([r]))

	def isinside(self, points):
		return np.logical_not(self.isoutside(points) )

	def isoutside(self, points):
		rc  = points - self.centroid   #centered points
		rct = np.asarray( np.matrix(self._ds._R) * np.matrix(rc).T).T  #centered and un-rotated points
		rad = (rct**2 / self.semi_axis_lengths**2).sum(axis=1)   #distance from center of centered, un-rotated and un-scaled points
		b   = float(rad) > 1   #check if points lie inside or outside the unit sphere
		return b




class _BivariateEllipse0D(_Ellipse):
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   alpha:              %.3f\n' %self.alpha
		s += '   centroid:           %s\n'   %self.centroid
		s += '   theta (deg):        %s\n'   %self.thetad
		s += '   major axis:         %s\n'   %self.Maxis
		s += '   minor axis:         %s\n'   %self.maxis
		s += '   semi axis lengths:  %s\n'   %[self.L0, self.L1]
		s += '   eccentricity:       %.3f\n' %self.eccentricity
		s += '------------------\n'
		s += str(self._ds)
		return s
	


	def ninside(self, r):
		return self.isinside(r).sum()
	def noutside(self, r):
		return self.isoutside(r).sum()
	
	def pinside(self, r):
		return self.isinside(r).mean()
	def poutside(self, r):
		return self.isoutside(r).mean()



	def plot(self, ax=None, n=51, **kwdargs):
		ax       = self._ds._gca(ax)
		x,y      = self.sample(n=51).T
		h        = ax.plot(x, y, label=self.label_short, **kwdargs)[0]
		return h
	
	def plot_patch(self, ax=None, **kwdargs):
		ax                = self._ds._gca(ax)
		Maxis             = self._ds.Maxis
		theta             = 180/pi * atan2(Maxis[1], Maxis[0])
		patch             = patches.Ellipse(self.centroid, 2*self.L0, 2*self.L1, theta)
		ax.add_patch(patch)
		plt.setp(patch, **kwdargs)
		return patch

	def plot_axes(self, ax=None, **kwdargs):
		ax          = self._ds._gca(ax)
		X0,Y0       = self.centroid - self.L0 * self.Maxis
		X1,Y1       = self.centroid + self.L0 * self.Maxis
		x0,y0       = self.centroid - self.L1 * self.maxis
		x1,y1       = self.centroid + self.L1 * self.maxis
		h0          = ax.plot((X0,X1), (Y0,Y1), '-', **kwdargs)
		h1          = ax.plot((x0,x1), (y0,y1), '-', **kwdargs)
		return h0,h1

	def plot_semi_axes(self, ax=None, **kwdargs):
		ax          = self._ds._gca(ax)
		X0,Y0       = self.centroid
		X1,Y1       = self.centroid + self.L0 * self.Maxis
		x0,y0       = self.centroid
		x1,y1       = self.centroid + self.L1 * self.maxis
		h0          = ax.plot((X0,X1), (Y0,Y1), '-', **kwdargs)
		h1          = ax.plot((x0,x1), (y0,y1), '-', **kwdargs)
		return h0,h1
		
	def sample(self, n=51):
		u     = np.linspace(0, 2*pi, n)
		x     = self.L0 * np.cos(u)
		y     = self.L1 * np.sin(u)
		r     = np.dot( np.vstack([x,y]).T , self._ds._R)
		return r + self.centroid




class _BivariateEllipse1D(_Ellipse):
	
	def __init__(self, ds, alpha=None):
		self._ds    = ds
		self.alpha  = 0.05 if alpha is None else alpha
		self.fwhm   = None
		self.L0     = None
		self.L1     = None
		self.set_alpha(alpha)
	
	
	def __repr__(self):
		s  = '%s\n' %self.__class__.__name__
		s += '   alpha:              %.3f\n' %self.alpha
		s += '------------------\n'
		s += str(self._ds)
		return s
	


	@property
	def semi_axis_lengths(self):
		return np.vstack([self.L0, self.L1]).T


	@property
	def theta(self):
		x,y = self.Maxis.T
		return np.arctan2(y, x)
	
	@property
	def thetad(self):
		return np.degrees(self.theta)

	def isinside(self, points):
		return not self.isoutside(points)
	
	def isoutside(self, points):
		rc  = points - self.centroid   #centered points
		L   = self.semi_axis_lengths
		b   = []
		for i in range(self._ds.Q):
			rct = np.asarray( np.matrix(self._ds._R[i]) * np.matrix(rc[i]).T).T  #centered and un-rotated points
			rad = (rct**2 / L[i]**2).sum(axis=1)   #distance from center of centered, un-rotated and un-scaled points
			bb  = float(rad) > 1   #check if points lie inside or outside the unit sphere
			b.append(bb)
		return np.any(b)
	
	def get_frame(self, frame):
		y   = self._ds.get_frame(frame)
		return self.Class0D(y, self.alpha)





class BivariateConfidenceEllipse0D(_BivariateEllipse0D):
	region_type       = 'confidence'
	region_type_short = 'CE'
	
	
	def set_alpha(self, alpha):
		p,n         = self._ds.I, self._ds.J              #counts: vector components, sample size
		df          = p, n - p                            #degrees of freedom (F statistic)
		F_crit      = stats.f.isf(alpha, df[0], df[1])    #critical F value
		T2_crit     = 2/(n-2) * F_crit / (n/(n-1))        #critical Hotelling's T2 value
		a,b         = np.sqrt(self._ds._s * T2_crit)      #ellipse axis lengths
		self.alpha  = alpha
		self.L0     = a
		self.L1     = b


class BivariateCI20D(_BivariateEllipse0D):
	region_type       = 'CI2'
	region_type_short = 'CI2'

	def set_alpha(self, alpha):
		k           = (-2*log(alpha))**.5
		ABCD        = self._ds.get_cov(bias=0)
		lam,IJKL    = np.linalg.eig(ABCD)
		lambdas     = np.matrix(np.diag(lam))
		theta       = np.arctan2(IJKL[1,:], IJKL[0,:])
		ind         = np.argsort(lam)
		axes        = (k * lam**0.5)[ind][::-1]
		self.alpha  = alpha
		self.L0     = axes[0]
		self.L1     = axes[1]


class BivariatePredictionEllipse0D(_BivariateEllipse0D):
	region_type       = 'prediction'
	region_type_short = 'PE'

	def set_alpha(self, alpha):
		p,n         = self._ds.I, self._ds.J
		fppf        = stats.f.ppf(1-alpha, p, n-p)*(n-1)*p*(n+1)/n/(n-p)
		a,b         = np.sqrt(self._ds._s * fppf)
		self.alpha  = alpha
		self.L0     = a
		self.L1     = b






class BivariateConfidenceEllipse1D(_BivariateEllipse1D):
	region_type       = 'confidence'
	region_type_short = 'CE'
	Class0D           = BivariateConfidenceEllipse0D
	
	def set_alpha(self, alpha):
		p,n         = self._ds.I, self._ds.J              #counts: vector components, sample size
		df          = p, n - p                            #degrees of freedom (F statistic)
		Q           = self._ds.Q
		m           = self._ds.mean                       #sample mean
		r           = self._ds.y - m                      #residuals
		efwhm       = rft1d.geom.estimate_fwhm(np.vstack([r[:,:,0], r[:,:,1]]))  #estimated smoothness
		F_crit      = rft1d.f.isf(alpha, df, Q, efwhm)  #critical F value
		T2_crit     = 2/(n-2) * F_crit / (n/(n-1))        #critical Hotelling's T2 value
		a,b         = np.sqrt(self._ds._s * T2_crit).T    #ellipse axis lengths
		self.alpha  = alpha
		self.fwhm   = efwhm
		self.L0     = a
		self.L1     = b



class BivariateCI21D(_BivariateEllipse1D):
	region_type       = 'ci2'
	region_type_short = 'ci2'
	Class0D           = BivariateCI20D

	def set_alpha(self, alpha, dmy=None):
		k           = (-2*log(alpha))**.5
		ABCD        = self._ds.get_cov(bias=0)
		L0,L1       = [],[]
		for abcd in ABCD:
			lam,IJKL    = np.linalg.eig(abcd)
			lambdas     = np.matrix(np.diag(lam))
			theta       = np.arctan2(IJKL[1,:], IJKL[0,:])
			ind         = np.argsort(lam)
			axes        = (k * lam**0.5)[ind][::-1]
			L0.append(axes[0])
			L1.append(axes[1])
		self.alpha  = alpha
		self.L0     = np.array(L0)
		self.L1     = np.array(L1)


class BivariatePredictionEllipse1D(_BivariateEllipse1D):
	region_type       = 'prediction'
	region_type_short = 'PE'
	Class0D           = BivariatePredictionEllipse0D

	def set_alpha(self, alpha):
		p,n         = self._ds.I, self._ds.J
		df          = p, n - p                            #degrees of freedom (F statistic)
		Q           = self._ds.Q
		m           = self._ds.mean                       #sample mean
		r           = self._ds.y - m                      #residuals
		efwhm       = rft1d.geom.estimate_fwhm(np.vstack([r[:,:,0], r[:,:,1]]))  #estimated smoothness
		fppf        = rft1d.f.isf(alpha, df, Q, efwhm) * (n-1)*p*(n+1)/n/(n-p)
		a,b         = np.sqrt(self._ds._s * fppf).T
		self.alpha  = alpha
		self.L0     = a
		self.L1     = b
		
		

