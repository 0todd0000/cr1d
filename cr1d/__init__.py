'''
cr1d: confidence and prediction regions for 0D and 1D uni-, bi- and tri-variate data.

version = {VERSION}


Copyright (C) 2020  Todd Pataky
'''


__version__  = '0.0.1'

# __doc__ = __doc__.replace('{VERSION}', __version__)



from . import colors
from . import data
from . dtypes import *
from . dtypes import Dataset
from . import ellipse
from . import plot
from . ui import *
from . import util



cmap              = colors.CR1DColorMap()
reset_color_cycle = colors.reset_color_cycle
set_color_cycle   = colors.set_color_cycle



Univariate0D = dtypes.Univariate0D
Univariate1D = dtypes.Univariate1D
Bivariate0D  = dtypes.Bivariate0D
Bivariate1D  = dtypes.Bivariate1D
Trivariate0D = dtypes.Trivariate0D
Trivariate1D = dtypes.Trivariate1D
