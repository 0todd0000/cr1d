'''
Base classes for all built-in datasets.

Copyright (C) 2020  Todd Pataky
'''





import os
import numpy as np



class ExpectedResults(object):
	df      = None   # degrees of freedom
	cr      = None   # 95% confidence region
	pr      = None   # 95% prediction region
	zstar   = None   # critical test statistic value

	def __repr__(self):
		s      = 'Expected Results\n'
		s     += f'   df              :  {self.df}\n'
		s     += f'   cr              :  {self.cr}\n'
		s     += f'   pr              :  {self.pr}\n'
		s     += f'   zstar           :  {self.zstar}\n'
		return s


class _CR1DDataset(object):
	_rtol             = 0.001  # relative tolerance (for unit tests)
	alpha             = 0.05
	design            = None   # design string (e.g. "One-way ANOVA")
	expected          = ExpectedResults() # expected results (for unit tests)
	m                 = None   # dependent variable dimensionality
	# mu                = None   # hypothesized population mean (if any)
	n                 = None   # domain dimensionality
	notes             = None   # dataset notes (if any)
	reference         = None   # literature reference (if it exists)
	url_datafile      = None   # link to data file on web (if any)
	url_description   = None   # link to data description on web (if any)
	y                 = None   # dependent variable values
	
	
	
	def __init__(self):
		self.y        = np.load( self.datafile )
	
	
	def __repr__(self):
		s      = 'CR1DDataset\n'
		s     += f'   name            :  {self.name}\n'
		s     += f'   design          :  {self.design}\n'
		s     += f'   dim             :  {self.dim}    (domain, dep.var.)\n'
		s     += f'   shape           :  {self.shape}\n'
		s     += f'   datafile        :  {self.datafile}\n'
		if self.url_description:
			s += f'   url_description :  {self.url_description}\n'
		if self.url_datafile:
			s += f'   url_datafile    :  {self.url_datafile}\n'
		if self.reference:
			s += f'   reference       :  {self.reference}\n'
		s     += f'------------------------\n'
		s     += str(self.expected) + '\n'
		if self.notes:
			s += f'--- NOTES --------------\n'
			s += f'   {self.notes}'
		return s
	
	@property
	def datafile(self):
		dir0  = os.path.dirname(__file__)
		fname = os.path.join(dir0, 'datafiles', f'{self.name}.npy')
		return fname
	@property
	def dim(self):
		return (self.n, self.m)
	@property
	def name(self):
		return self.__class__.__name__
	@property
	def shape(self):
		return self.y.shape
	
	
	def get_dependent_variable(self):
		return self.y
	
	def get_dv(self):
		return self.y
	
	
	# def _printR(self, x, name='x'):
	# 	print( '%s = c(%s)' %(name, str(x.tolist())[1:-1]) )
	# def _printRs(self, xx, names=('x')):
	# 	for x,name in zip(xx,names):
	# 		print
	# 		self._printR(x, name)
	# def _set_values(self):    #abstract method;  instantiated by all subclasses
	# 	pass
	# def get_dependent_variable(self):
	# 	return self.Y
	# def get_expected_df(self):
	# 	return self.df
	# def get_data(self):
	# 	return self.Y
	# def get_expected_test_stat(self):
	# 	return self.z
	# def get_expected_p_value(self):
	# 	return self.p
	# def get_expected_results_as_string(self):
	# 	s      = '  (Expected results)\n'
	# 	s     += '  %s         :  %s\n' %("{:<2}".format(self.STAT), str(self.z))
	# 	if self.df is not None:
	# 		s += '  df         :  %s\n' %str(self.df)
	# 	s     += '  p          :  %s\n' %str(self.p)
	# 	return s





