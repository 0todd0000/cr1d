
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


_cycle_default = deepcopy( plt.rcParams['axes.prop_cycle'] )


def reset_color_cycle():
	set_color_cycle('default')

def set_color_cycle(cyclename=None):
	cyclename = 'cr1d' if (cyclename is None) else cyclename
	setter    = ColorCycleSetter()
	setter.set_cycle( cyclename )




class ColorCycleSetter(object):
	def __init__(self):
		self.cycle_default = _cycle_default
		self.cycle_cr1d    = plt.cycler( color=CR1DColorMap().hex )
		
	def set_cycle(self, cyclename='cr1d'):
		if cyclename not in ['cr1d', 'default']:
			raise ValueError('"cyclename" must be "cr1d" or "default"')
		cycle = self.cycle_cr1d if (cyclename == 'cr1d') else self.cycle_default
		plt.rcParams['axes.prop_cycle'] = cycle


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





	

