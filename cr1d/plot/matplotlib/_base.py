
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection






class PatchLine(object):


	def plot(self, ax, w=0.1, ec=None, fc='b', lw=1):
		self.w  = float(w)
		verts,edges,faces  = self.get_geometry()
		patches = [Polygon(verts[f]) for f in faces]
		coll    = PatchCollection(patches)
		ax.add_collection( coll )
		plt.setp(patches)
		plt.setp(coll, alpha=0.5, facecolor=fc, lw=lw, edgecolor=ec)
		ax.autoscale()
		return patches




class MultiColorPatchLine(PatchLine):

	def plot(self, ax, w=0.1, cmap='jet', alpha=0.5, ec=None, ew=1, vmin=None, vmax=None, th=None):
		self.w  = float(w)
		verts,edges,faces  = self.get_geometry()
		patches = [Polygon(verts[f]) for f in faces]
		coll    = PatchCollection(patches)
		ax.add_collection( coll )
		plt.setp(patches)
		# set face colors:
		vmin   = self.z.min() if (vmin is None) else vmin
		vmax   = self.z.max() if (vmax is None) else vmax
		# threshold:
		z      = self.z.copy()
		if th is not None:
			# z[z<th] = vmin
			z[z<th] = np.nan
		zn     = (z-vmin) / (vmax-vmin)
		# set colormap:
		if cmap in ['spm', 'spm_warm', 'spm_cool']:
			spmcm = SPMColormapBuilder()
			cmap  = eval('spmcm.%s()'%cmap)
		else:
			cmap  = eval('plt.cm.%s'%cmap)
		# cmap.set_bad(color='b', alpha=0.5)
		cmap.set_under(color='0.9', alpha=0.5)
		# cmap.set_over(color='b', alpha=0.5)
		
		colors = cmap( zn )
		# plt.setp(coll, alpha=alpha, facecolor=colors, lw=ew, edgecolor=ec)
		plt.setp(coll, facecolor=colors, lw=ew, edgecolor=ec)
		ax.autoscale()
		return patches







