
from . _base import _CR1DDataset






# class FraminghamSystolicBloodPressure(_base.DatasetCIpaired):
# 	def _set_values(self):
# 		self.www      = 'http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/BS704_Confidence_Intervals/BS704_Confidence_Intervals_print.html'
# 		self.YA       = np.array([141, 119, 122, 127, 125, 123, 113, 106, 131, 142, 131, 135, 119, 130, 121], dtype=float)
# 		self.YB       = np.array([168, 111, 139, 127, 155, 115, 125, 123, 130, 137, 130, 129, 112, 141, 122], dtype=float)
# 		self.alpha    = 0.05
# 		self.mu       = 0
# 		self.ci       = (-12.4, 1.8)
# 		self.note     = 'Note     ', 'From "Confidence Intervals for Matched Samples, Continuous Outcome" at the link above.'


class FraminghamSystolicBloodPressure(_CR1DDataset):
	def __init__(self):
		super().__init__()
		self.alpha            = 0.05
		self.design           = 'Paired'
		self.n                = 0   # domain dimensionality
		self.m                = 1   # DV dimensionality
		self.url_datafile     = None
		self.url_description  = 'http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/BS704_Confidence_Intervals/BS704_Confidence_Intervals_print.html'
		self.notes            = 'Note     ', 'From "Confidence Intervals for Matched Samples, Continuous Outcome" at the link above.'
		self.expected.cr      = (-12.4, 1.8)





class MinnesotaGeyerRate(_CR1DDataset):
	def __init__(self):
		super().__init__()
		self.alpha            = 0.05
		self.design           = 'One-sample'
		self.n                = 0   # domain dimensionality
		self.m                = 1   # DV dimensionality
		self.url_datafile     = 'http://www.stat.umn.edu/geyer/3011/mdata/chap16/eg16-01.dat'
		self.url_description  = 'http://www.stat.umn.edu/geyer/3011/examp/conf.html'
		self.notes            = None
		self.expected.cr      = (21.52709, 29.80625)
		
		



class WebsterSleep(_CR1DDataset):
	def __init__(self):
		super().__init__()
		self.alpha            = 0.05
		self.design           = 'One-sample'
		self.n                = 0   # domain dimensionality
		self.m                = 1   # DV dimensionality
		self.url_datafile     = None
		self.url_description  = 'http://faculty.webster.edu/woolflm/ci.html'
		self.notes            = 'Note     ', 'The expected CI may be slightly incorrect due to rounding errors.'
		self.expected.cr      = (8.50, 13.33)

