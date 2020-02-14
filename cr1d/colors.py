
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


class CR1DColorMap(object):
	
	rgb = [
		(148,202,130),
		(150,179,221),
		(187,147,194),
		(153,156,205),
		(126,206,244),
		(127,197,194),
		(127,156,172),
		(192,163,108),
	]
	
	def __init__(self, set_color_cycler=True):
		if set_color_cycler:
			plt.rcParams['axes.prop_cycle'] = plt.cycler(color=self.hex)
		
	
	@property
	def name(self):
		return self.__class__.__name__
	@property
	def cmap(self, bgcolor=None):
		return colors.LinearSegmentedColormap.from_list(self.name, self.rgb01)
	@property
	def hex(self):
		return [colors.rgb2hex(c) for c in self.rgb01]
	@property
	def rgb01(self, bgcolor=None):
		return 1.0/255 * np.asarray(self.rgb)

	def colors(self, n):
		return self.cmap( np.linspace(0, 255, n) )

	def colorbar_image(self, n=256, vertical=True):
		I     = np.vstack([range(n)]*10)
		if vertical:
			I = I.T
		return I
		
	def set_prop_cycle(self, ax):
		ax.set_prop_cycle(color=self.hex)






