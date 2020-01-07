
from . _base import _CR1DDataset


class MinnesotaGeyerRate(_CR1DDataset):
	def __init__(self):
		super().__init__()
		self.design           = 'One-sample'
		self.n                = 0
		self.m                = 1
		self.url_datafile     = 'http://www.stat.umn.edu/geyer/3011/mdata/chap16/eg16-01.dat'
		self.url_description  = 'http://www.stat.umn.edu/geyer/3011/examp/conf.html'
		self.notes            = None
		self.expected.cr      = (21.52709, 29.80625)
		
		



# class WebsterSleep(object):
# 	def _set_values(self):
# 		self.www   = 'http://faculty.webster.edu/woolflm/ci.html'
# 		self.Y     = np.array([4.5, 22, 7, 14.5, 9, 9, 3.5, 8, 11, 7.5, 18, 20, 7.5, 9, 10.5, 15, 19, 2.5, 5, 9, 8.5, 14, 20, 8])
# 		self.alpha = 0.05
# 		self.mu    = None
# 		self.ci    = (8.50, 13.33)
# 		self.note  = 'Note     ', 'The expected CI may be slightly incorrect due to rounding errors.'
