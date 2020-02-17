

from IPython import get_ipython


isjupyter = 'zmqshell' in str( type( get_ipython() ) )



if isjupyter:
	from . plotly import DatasetPlotter
	from . plotly import colors
	# from . matplotlib import DatasetPlotter
	# from . matplotlib import colors

else:
	from . matplotlib import DatasetPlotter
	from . matplotlib import colors




