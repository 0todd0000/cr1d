

from IPython import get_ipython


isjupyter = 'zmqshell' in str( type( get_ipython() ) )



if isjupyter:
	pass
	# from . plotly import DatasetPlotter

else:
	from . matplotlib import DatasetPlotter
	from . matplotlib import colors




