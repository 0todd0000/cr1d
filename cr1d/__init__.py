'''
cr1d: confidence and prediction regions for 0D and 1D uni-, bi- and tri-variate data.

version = {VERSION}


Copyright (C) 2020  Todd Pataky
'''


__version__  = '0.0.1'

# __doc__ = __doc__.replace('{VERSION}', __version__)



from . import data
from . import datasetdefs as ds
from . import ellipse,plot

BivariateDataset0D  = ds.BivariateDataset0D
BivariateDataset1D  = ds.BivariateDataset1D
UnivariateDataset0D = ds.UnivariateDataset0D
UnivariateDataset1D = ds.UnivariateDataset1D