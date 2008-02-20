import matplotlib
matplotlib.use('GTK')

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matplotlib.backends.backend_gtk \
	import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtk \
	import NavigationToolbar2GTK as NavigationToolbar

from gandalf.base import Object

class Plot(Object):

	xandys = []

	def set_window(self, window):
		Object.set_window(self, window)
		widget = self.xml.get_widget("window")

		self.toolbar = NavigationToolbar(self.canvas, widget)
		self.toolbar.show()

		widget = self.xml.get_widget("plot_vbox")
		widget.pack_start(self.canvas)
		widget.pack_start(self.toolbar, False, False)

	def set_limits(self, xmin=None, xmax=None, ymin=None, ymax=None):
		if xmin is not None:
			widget = self.xml.get_widget("plot_xmin_entry")
			widget.set_text(str(xmin))

		if xmax is not None:
			widget = self.xml.get_widget("plot_xmax_entry")
			widget.set_text(str(xmax))

		if ymin is not None:
			widget = self.xml.get_widget("plot_ymin_entry")
			widget.set_text(str(ymin))

		if ymax is not None:
			widget = self.xml.get_widget("plot_ymax_entry")
			widget.set_text(str(ymax))

	def plot(self, x, y, style, color=0xFF0000, xlabel=None, ylabel=None):
		conv = lambda elem: str(elem)
		self.xandys = zip(map(conv, x), map(conv, y))

		if xlabel != None: self.subplot.set_xlabel(xlabel)
		if ylabel != None: self.subplot.set_ylabel(ylabel)

		t = self.window.btask("plot plot")

		self.subplot.plot(x, y, style, color='#%06X' % (color))
		self.subplot.grid(True)

		self.window.etask("plot plot", t)

	def plotr(self, *args, **kwargs):
		self.figure.sca(self.axr)
		if not kwargs.has_key('color'):
			kwargs['color'] = 0x00FF00
		self.plot(*args, **kwargs)

	def plotl(self, *args, **kwargs):
		self.figure.sca(self.axl)
		if not kwargs.has_key('color'):
			kwargs['color'] = 0xFF0000
		self.plot(*args, **kwargs)

	def ploth(self, y, style='--', color=0xFF0000):
		t = self.window.btask("plot ploth")

		self.subplot.axhline(y, ls=style, color='#%06X' % (color))
		self.subplot.grid(True)

		self.window.etask("plot ploth", t)

	def plotv(self, x, style='--', color=0xFF0000):
		t = self.window.btask("plot plotv")

		self.subplot.axvline(x, ls=style, color='#%06X' % (color))
		self.subplot.grid(True)

		self.window.etask("plot plotv", t)

	def draw(self):
		self.subplot.axis('auto')

		if (self.xmin != 0 or self.xmax != 0 or self.ymin != 0 or self.ymax != 0):
			self.subplot.axis([self.xmin, self.xmax, self.ymin, self.ymax])

		t = self.window.btask("plot draw")
		self.canvas.draw()
		self.window.etask("plot draw", t)

	def clear(self):
		if self.props.plot.overlay:
			return

		t = self.window.btask("plot clear")
		self.subplot.clear()
		self.window.etask("plot clear", t)

		self.subplot.grid(True)

	def saveas(self, filename):
		f = open(filename, 'w')
		f.writelines([",".join(xandy) + "\n" for xandy in self.xandys])
		f.close()

	def __init__(self):
		self.figure = Figure()

		self.axl = self.figure.gca()
		self.axl.yaxis.set_label_position('left')
		self.axl.yaxis.tick_left()

		self.axr = self.figure.add_axes(self.axl.get_position(), sharex=self.axl, frameon=False)
		self.axr.yaxis.set_label_position('right')
		self.axr.yaxis.tick_right()

		self.subplot = self.figure.add_subplot(111)
		self.subplot.grid(True)

		self.canvas = FigureCanvas(self.figure)
		self.canvas.show()

		self.xmin = 0
		self.xmax = 0
		self.ymin = 0
		self.ymax = 0
