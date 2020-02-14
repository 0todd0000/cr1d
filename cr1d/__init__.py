'''
cr1d: confidence and prediction regions for 0D and 1D uni-, bi- and tri-variate data.

version = {VERSION}


Copyright (C) 2020  Todd Pataky
'''


__version__  = '0.0.1'

# __doc__ = __doc__.replace('{VERSION}', __version__)



from . import data
from . colors import CR1DColorMap
from . dtypes import *
from . import ellipse
from . import plot
from . ui import *
from . util import *



cmap = CR1DColorMap(set_color_cycler=True)


# BivariateDataset0D  = dtypes.Bivariate0D
# BivariateDataset1D  = dtypes.Bivariate1D
# UnivariateDataset0D = dtypes.Univariat0D
# UnivariateDataset1D = dtypes.Univariat1D