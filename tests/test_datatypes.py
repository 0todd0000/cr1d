
import unittest
import numpy as np
import cr1d
 


class TestAutoDatasetType(unittest.TestCase):
	def test_univariate_0d(self):
		y = np.random.randn(10)
		d = cr1d.Dataset(y)
		assert isinstance(d, cr1d.Univariate0D)

	def test_bivariate_0d(self):
		y = np.random.randn(10,2)
		d = cr1d.Dataset(y)
		assert isinstance(d, cr1d.Bivariate0D)

	def test_trivariate_0d(self):
		y = np.random.randn(10,3)
		d = cr1d.Dataset(y)
		assert isinstance(d, cr1d.Trivariate0D)

	def test_univariate_1d(self):
		y0 = np.random.randn(10,100)
		y1 = np.random.randn(7,10)
		d0 = cr1d.Dataset(y0)
		d1 = cr1d.Dataset(y1)
		assert isinstance(d0, cr1d.Univariate1D)
		assert isinstance(d1, cr1d.Univariate1D)

	def test_bivariate_1d(self):
		y0 = np.random.randn(10,100,2)
		y1 = np.random.randn(7,10,2)
		d0 = cr1d.Dataset(y0)
		d1 = cr1d.Dataset(y1)
		assert isinstance(d0, cr1d.Bivariate1D)
		assert isinstance(d1, cr1d.Bivariate1D)

	def test_trivariate_1d(self):
		y0 = np.random.randn(10,100,3)
		y1 = np.random.randn(7,10,3)
		d0 = cr1d.Dataset(y0)
		d1 = cr1d.Dataset(y1)
		assert isinstance(d0, cr1d.Trivariate1D)
		assert isinstance(d1, cr1d.Trivariate1D)






if __name__ == '__main__':
	unittest.main()