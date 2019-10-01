'''
Utility plotting functions and custom colormap definitions.
'''

from copy import copy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap
import spm1d


class SPMColormapBuilder(object):

	cdict = {'red': ((0.0, 1.0, 1.0),
					(0.15, 0.0, 0.0),
					(0.5, 0.0, 0.0),
					(0.7, 1.0, 1.0),
					(1.0, 1.0, 1.0)),

		'green': ((0.0, 1.0, 1.0),
		        (0.1, 1.0, 1.0),
				(0.3, 0.0, 0.0),
				(0.5, 0.0, 0.0),
				(0.7, 0.0, 0.0),
				(0.9, 1.0, 1.0),
				(1.0, 1.0, 1.0)),

		'blue': ((0.0, 1.0, 1.0),
				(0.3, 1.0, 1.0),
				(0.5, 0.0, 0.0),
				(0.85, 0.0, 0.0),
				(1.0, 1.0, 1.0))}
			
	@staticmethod
	def _get_cmap(d, bgcolor=None):
		cmap = LinearSegmentedColormap('my_colormap', d, 256)
		if bgcolor is not None:
			cmap.set_bad(color=bgcolor, alpha=1)
		return cmap

	def spm(self, bgcolor=None):
		return self._get_cmap(self.cdict, bgcolor)

	def spm_cool(self, bgcolor=None):
		d           = copy(self.cdict)
		r,g,b       = [np.array(d[s])  for s in ('red', 'green', 'blue')]
		inds        = [int(np.argwhere(x[:,0]==0.5)) for x in (r,g,b)]
		r,g,b       = [np.flipud(x[:i+1]) for x,i in zip((r,g,b),inds)]
		r[:,0]      = np.linspace(0, 1, r.shape[0])
		g[:,0]      = np.linspace(0, 1, g.shape[0])
		b[:,0]      = np.linspace(0, 1, b.shape[0])
		d['red']    = r
		d['green']  = g
		d['blue']   = b
		return self._get_cmap(d, bgcolor)

	def spm_warm(self, bgcolor=None):
		d          = copy(self.cdict)
		r,g,b      = [np.array(d[s])  for s in ('red', 'green', 'blue')]
		inds       = [int(np.argwhere(x[:,0]==0.5)) for x in (r,g,b)]
		r,g,b      = [x[i:] for x,i in zip((r,g,b),inds)]
		r[:,0]     = np.linspace(0, 1, r.shape[0])
		g[:,0]     = np.linspace(0, 1, g.shape[0])
		b[:,0]     = np.linspace(0, 1, b.shape[0])
		d['red']   = r
		d['green'] = g
		d['blue']  = b
		return self._get_cmap(d, bgcolor)



def plot_ci2style(ax, rA, rB, cmap=None, lw=3, vmin=None, vmax=None, thresholded=False):
	cmap    = 'jet' if (cmap is None) else cmap
	spm     = spm1d.stats.hotellings2(rA, rB)
	z       = spm.z
	th      = spm.inference(0.05).zstar if thresholded else None
	mA,mB   = rA.mean(axis=0), rB.mean(axis=0)
	plot_multicolorline(ax, mA[:,0], mA[:,1], z=z, cmap=cmap, lw=lw, vmin=vmin, vmax=vmax, th=th)
	plot_multicolorline(ax, mB[:,0], mB[:,1], z=z, cmap=cmap, lw=lw, vmin=vmin, vmax=vmax, th=th)
	ax.set_facecolor('0.9')
	
	
	
	


def plot_multicolorline(ax, x, y, z=None, cmap='jet', lw=3, vmin=None, vmax=None, th=None):
	'''
	Follows the Matplotlib cookbook code:
	https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/multicolored_line.html
	
	ax   : matplotlib axis
	x    : x values
	y    : y values
	z    : scalars representing colors in a color map (default: y)
	cmap : matplotlib colormap (default: jet)
	lw   : line width
	vmin : minimum value of the colormap (default : min(y) )
	vmax : maximum value of the colormap (default : max(y) )
	th   : threshold (all z value less than th will be assigned values of vmin)
	'''
	### set default parameter values:
	z         = y.copy() if (z is None) else z
	vmin      = z.min() if (vmin is None) else vmin
	vmax      = z.max() if (vmax is None) else vmax
	### set the colormap:
	if cmap in ['spm', 'spm_warm', 'spm_cool']:
		spmcm = SPMColormapBuilder()
		cmap  = eval('spmcm.%s()'%cmap)
	### threshold the colors:
	if th is not None:
		z[z<th] = vmin
	### create line segments:
	points    = np.array([x, y]).T.reshape(-1, 1, 2)
	segments  = np.concatenate([points[:-1], points[1:]], axis=1)
	norm      = plt.Normalize(vmin, vmax)
	lc        = LineCollection(segments, cmap=cmap, norm=norm)
	lc.set_array(z)
	lc.set_linewidth(lw)
	line      = ax.add_collection(lc)
	ax.autoscale()
	# dmy       = ax.plot(x, y)[0]
	# dmy.set_visible(False)
	return line
		

