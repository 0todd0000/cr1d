
from . _base import _CR1DDataset






class AnimalsInResearch(_CR1DDataset):
	def __init__(self):
		super().__init__()
		self.alpha            = 0.05
		self.design           = 'Two-sample'
		self.n                = 0   # domain dimensionality
		self.m                = 1   # DV dimensionality
		self.url_datafile     = 'http://onlinestatbook.com/2/case_studies/animal_research.html'
		self.url_description  = 'http://onlinestatbook.com/2/estimation/difference_means.html'
		self.notes            = 'Note     ', 'To access the original data visit the "data file" link and select "Show Data" from the bottom of the page.'
		self.expected.cr      = (0.29, 2.65)



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

