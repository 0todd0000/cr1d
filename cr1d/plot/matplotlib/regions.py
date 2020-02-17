



def plot_multicolorline(ax, x, y, z=None, cmap='jet', alpha=0.5, w=0.1, ec=None, ew=1, vmin=None, vmax=None, th=None):
	mcl = MultiColorPatchLine(x, y, z)
	mcl.plot(ax, cmap=cmap, alpha=alpha, w=w, ec=ec, ew=ew, vmin=vmin, vmax=vmax, th=th)




# def plot_ci2style(ax, rA, rB, cmap=None, alpha=0.5, lw=3, vmin=None, vmax=None, thresholded=False):
# 	cmap    = 'jet' if (cmap is None) else cmap
# 	spm     = spm1d.stats.hotellings2(rA, rB)
# 	z       = spm.z
# 	th      = spm.inference(0.05).zstar if thresholded else None
# 	mA,mB   = rA.mean(axis=0), rB.mean(axis=0)
# 	plot_multicolorline(ax, mA[:,0], mA[:,1], z=z, cmap=cmap, alpha=alpha, lw=lw, vmin=vmin, vmax=vmax, th=th)
# 	plot_multicolorline(ax, mB[:,0], mB[:,1], z=z, cmap=cmap, alpha=alpha, lw=lw, vmin=vmin, vmax=vmax, th=th)
# 	ax.set_facecolor('0.9')


def plot_ci2style(ax, rA, rB, cmap=None, alpha=0.5, vmin=None, vmax=None, thresholded=False):
	cmap    = 'jet' if (cmap is None) else cmap
	spm     = spm1d.stats.hotellings2(rA, rB)
	z       = spm.z
	th      = spm.inference(0.05).zstar if thresholded else None
	mA,mB   = rA.mean(axis=0), rB.mean(axis=0)
	plot_multicolorline(ax, mA[:,0], mA[:,1], z=z, cmap=cmap, alpha=alpha, vmin=vmin, vmax=vmax, th=th)
	plot_multicolorline(ax, mB[:,0], mB[:,1], z=z, cmap=cmap, alpha=alpha, vmin=vmin, vmax=vmax, th=th)
	ax.set_facecolor('0.9')

