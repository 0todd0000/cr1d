'''
Utility plotting functions and custom colormap definitions.
'''

from copy import copy
from math import pi,sin,acos
import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib.patches import Polygon
# from matplotlib.collections import PatchCollection





class PatchLine(object):
	def __init__(self, x, y):
		self.x             = np.asarray(x, dtype=float).copy()
		self.y             = np.asarray(y, dtype=float).copy()
		self.w             = None  #patchline width (set when calling "plot")
		self.normals       = np.array([self._get_segment_normal(self.x[i:i+2], self.y[i:i+2])  for i in range(self.nseg)])
		self.ends          = None   #None, "horizontal" or "vertical"

	@property
	def nnodes(self):
		return self.x.size
	@property
	def nseg(self):
		return self.nnodes - 1
	
	
	def _get_segment_normal(self, x, y):
		(x0,x1),(y0,y1) = x, y
		r  = np.array([-(y1-y0), x1-x0])
		r /= np.linalg.norm(r)
		return r

	def get_edges(self):
		N      = self.nnodes
		### x direction:
		edge0  = np.vstack([range(N-1), range(1,N)]).T
		edge1  = edge0 + N
		edge2  = edge0 + 2*N
		edge3  = edge0 + 3*N
		edgesX = np.vstack([edge0,edge1,edge2,edge3])
		### y direction:
		x      = np.arange(N)
		edge0  = np.vstack([x, x+N]).T
		edge1  = edge0 + 2*N
		edgesY = np.vstack([edge0,edge1])
		### z direction:
		edge0  = np.vstack([x, x+2*N]).T
		edge1  = edge0+N
		edgesZ = np.vstack([edge0,edge1])
		### combine all:
		edges  = np.vstack([edgesX, edgesY, edgesZ])
		return edges.tolist()


	def get_faces(self):
		N        = self.nnodes
		nFaces   = N-1
		faces    = (np.array([[0,1,N+1,N]]*nFaces).T + range(nFaces)).T
		return faces

	def get_geometry(self):
		rL,rU          = self.get_vertices()
		verts          = np.vstack([rL,rU,rL,rU])
		edges          = self.get_edges()
		faces          = self.get_faces()
		return verts,edges,faces

	def get_endpoints(self):
		(x0,x1),(y0,y1) = self.x[-2:], self.y[-2:]
		xy0,xy1         = np.array([x0,y0]), np.array([x1,y1])
		if self.ends is None:
			n           = self.w * self.normals[-1]
		elif self.ends == 'vertical':
			n           = [0, self.w / np.dot(self.normals[-1],[0,1])]
		elif self.ends == 'horizontal':
			n = [self.w / np.dot(self.normals[-1],[1,0]), 0]
		r0,r1           = xy1-n, xy1+n
		return np.vstack([r0,r1])

	def get_startpoints(self):
		(x0,x1),(y0,y1) = self.x[:2], self.y[:2]
		xy0,xy1         = np.array([x0,y0]), np.array([x1,y1])
		if self.ends is None:
			n           = self.w * self.normals[0]
		elif self.ends == 'vertical':
			n           = [0, self.w / np.dot(self.normals[0],[0,1])]
		elif self.ends == 'horizontal':
			n = [self.w / np.dot(self.normals[0],[1,0]), 0]
		r0,r1           = xy0-n, xy0+n
		return np.vstack([r0,r1])

	def get_intersections(self):
		Rupper,Rlower   = [],[]
		for i in range(self.nseg-1):
			n0,n1       = self.normals[i], self.normals[i+1]
			u           = n0 + n1
			u          /= np.linalg.norm(u)
			beta        = acos( np.dot(n0,n1) )
			theta       = 0.5 * (pi - beta)
			c           = self.w / sin(theta)
			r1          = np.array([self.x[i+1], self.y[i+1]])
			rupper      = r1 + c*u
			rlower      = r1 - c*u
			Rupper.append(rupper)
			Rlower.append(rlower)
		return np.array(Rupper), np.array(Rlower)

	def get_vertices(self):
		r0L,r0U      = self.get_startpoints()
		rU,rL        = self.get_intersections()
		r1L,r1U      = self.get_endpoints()
		rL           = np.vstack([r0L,rL,r1L])
		rU           = np.vstack([r0U,rU,r1U])
		return rL,rU

	# def plot(self, ax, w=0.1, ec=None, fc='b', lw=1):
	# 	self.w  = float(w)
	# 	verts,edges,faces  = self.get_geometry()
	# 	patches = [Polygon(verts[f]) for f in faces]
	# 	coll    = PatchCollection(patches)
	# 	ax.add_collection( coll )
	# 	plt.setp(patches)
	# 	plt.setp(coll, alpha=0.5, facecolor=fc, lw=lw, edgecolor=ec)
	# 	ax.autoscale()
	# 	return patches




class MultiColorPatchLine(PatchLine):
	def __init__(self, x, y, z=None):
		super().__init__(x, y)
		self.z             = np.linspace(0, 1, self.nnodes) if (z is None) else np.asarray(z, dtype=float).copy()
	
	# def plot(self, ax, w=0.1, cmap='jet', alpha=0.5, ec=None, ew=1, vmin=None, vmax=None, th=None):
	# 	self.w  = float(w)
	# 	verts,edges,faces  = self.get_geometry()
	# 	patches = [Polygon(verts[f]) for f in faces]
	# 	coll    = PatchCollection(patches)
	# 	ax.add_collection( coll )
	# 	plt.setp(patches)
	# 	# set face colors:
	# 	vmin   = self.z.min() if (vmin is None) else vmin
	# 	vmax   = self.z.max() if (vmax is None) else vmax
	# 	# threshold:
	# 	z      = self.z.copy()
	# 	if th is not None:
	# 		# z[z<th] = vmin
	# 		z[z<th] = np.nan
	# 	zn     = (z-vmin) / (vmax-vmin)
	# 	# set colormap:
	# 	if cmap in ['spm', 'spm_warm', 'spm_cool']:
	# 		spmcm = SPMColormapBuilder()
	# 		cmap  = eval('spmcm.%s()'%cmap)
	# 	else:
	# 		cmap  = eval('plt.cm.%s'%cmap)
	# 	# cmap.set_bad(color='b', alpha=0.5)
	# 	cmap.set_under(color='0.9', alpha=0.5)
	# 	# cmap.set_over(color='b', alpha=0.5)
	#
	# 	colors = cmap( zn )
	# 	# plt.setp(coll, alpha=alpha, facecolor=colors, lw=ew, edgecolor=ec)
	# 	plt.setp(coll, facecolor=colors, lw=ew, edgecolor=ec)
	# 	ax.autoscale()
	# 	return patches







