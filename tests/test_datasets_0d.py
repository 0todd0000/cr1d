

import unittest
import numpy as np
import cr1d
 

# class TestDatasetLoading(unittest.TestCase):
#
#
# 	def test_a(self):
# 		dataset = cr1d.data.MinnesotaGeyerRate()



class TestExpectedResults(unittest.TestCase):
	def test_MinnesotaGeyerRate(self):
		dataset = cr1d.data.MinnesotaGeyerRate()
		y       = dataset.y
		cr      = cr1d.confidence_region(y)
		np.testing.assert_array_almost_equal(cr.interval, dataset.expected.cr, decimal=5)

	def test_WebsterSleep(self):
		dataset = cr1d.data.WebsterSleep()
		y       = dataset.y
		cr      = cr1d.confidence_region(y)
		np.testing.assert_array_almost_equal(cr.interval, dataset.expected.cr, decimal=1)




if __name__ == '__main__':
	unittest.main()