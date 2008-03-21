# standard python libraries
import os

# matplotlib.sf.net
import matplotlib
matplotlib.use('GTK')

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from matplotlib.backends.backend_gtk \
	import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtk \
	import NavigationToolbar2GTK as NavigationToolbar

# www.gtk.org
import gobject
import gtk
import gtk.glade

# our own libraries
from kochanski.util import Object, Property

class Common(Object):

	def saveas(self, filename, xandys):
		f = open(filename, 'w')
		f.writelines([','.join(xandy) + '\n' for xandy in xandys])
		f.close()

	def __init__(self):
		Object.__init__(self)

class Console(Common):

	def show(self, *args, **kwargs):
		pass

	def hide(self, *args, **kwargs):
		pass

	def run(self, *args, **kwargs):
		pass

	def __plot(self, x, y, style=None, color=0xFF0000, xlabel=None, ylabel=None):
		for i, v in enumerate(x):
			print 'index:', i
			print 'x, y = %.4f, %4f' % (x[i], y[i])

	def plotr(self, *args, **kwargs):
		self.__plot(*args, **kwargs)

	def plotl(self, *args, **kwargs):
		self.__plot(*args, **kwargs)

	def ploth(self, *args, **kwargs):
		self.__plot(*args, **kwargs)

	def plotv(self, *args, **kwargs):
		self.__plot(*args, **kwargs)

	def draw(self, *args, **kwargs):
		pass

	def clear(self, *args, **kwargs):
		pass

class Backend(Object):

	def show(self):
		self.__canvas.show()
		self.__toolbar.show()
		self.widget.show()

	def hide(self):
		self.widget.hide()
		self.__toolbar.hide()
		self.__canvas.hide()

	def __plot(self, x, y, style='-', color=0xFF0000, xlabel=None, ylabel=None):
		conv = lambda elem: str(elem)
		self.xandys = zip(map(conv, x), map(conv, y))

		if xlabel != None: self.__subplot.set_xlabel(xlabel)
		if ylabel != None: self.__subplot.set_ylabel(ylabel)

		self.__subplot.plot(x, y, style, color='#%06X' % (color))
		self.__subplot.grid(True)

	def plotr(self, *args, **kwargs):
		self.__figure.sca(self.__axr)
		if kwargs.has_key('color') is False:
			kwargs['color'] = 0x00FF00
		self.__plot(*args, **kwargs)

	def plotl(self, *args, **kwargs):
		self.__figure.sca(self.__axl)
		if kwargs.has_key('color') is False:
			kwargs['color'] = 0xFF0000
		self.__plot(*args, **kwargs)

	def ploth(self, y, style='--', color=0xFF0000):
		self.__subplot.axhline(y, ls=style, color='#%06X' % (color))
		self.__subplot.grid(True)

	def plotv(self, x, style='--', color=0xFF0000):
		self.__subplot.axvline(x, ls=style, color='#%06X' % (color))
		self.__subplot.grid(True)

	def draw(self):
		self.__subplot.axis('auto')

		if (self.xmin != 0 or self.xmax != 0 or self.ymin != 0 or self.ymax != 0):
			self.__subplot.axis([self.xmin, self.xmax, self.ymin, self.ymax])

		self.__canvas.draw()

	def clear(self):
		self.__subplot.clear()
		self.__subplot.grid(True)

	def __init__(self):
		self.__figure = Figure()

		self.__axl = self.__figure.gca()
		self.__axl.yaxis.set_label_position('left')
		self.__axl.yaxis.tick_left()

		self.__axr = self.__figure.add_axes(self.__axl.get_position(), sharex=self.__axl, frameon=False)
		self.__axr.yaxis.set_label_position('right')
		self.__axr.yaxis.tick_right()

		self.__subplot = self.__figure.add_subplot(111)
		self.__subplot.grid(True)

		self.widget = gtk.VBox() # widget must be a GTK+ widget

		self.__canvas = FigureCanvas(self.__figure)
		self.widget.pack_start(self.__canvas)

		self.__toolbar = NavigationToolbar(self.__canvas, None)
		self.widget.pack_start(self.__toolbar, False, False)

		self.xandys = []

class Window(Common):

	@Property
	def xmin():
		def fget(self):
			if self.__backend is None:
				return None

			return self.__backend.xmin
				
		def fset(self, xmin):
			if self.__backend is None:
				return

			self.__backend.xmin = xmin

			if self.__widgets is None:
				return

			widget = self.__widgets.get_widget('preferences_xmin_entry')
			widget.set_text(str(xmin))

		return locals()

	@Property
	def xmax():
		def fget(self):
			if self.__backend is None:
				return None

			return self.__backend.xmax
				
		def fset(self, xmax):
			if self.__backend is None:
				return

			self.__backend.xmax = xmax

			if self.__widgets is None:
				return

			widget = self.__widgets.get_widget('preferences_xmax_entry')
			widget.set_text(str(xmax))

		return locals()

	@Property
	def ymin():
		def fget(self):
			if self.__backend is None:
				return None

			return self.__backend.ymin
				
		def fset(self, ymin):
			if self.__backend is None:
				return

			self.__backend.ymin = ymin

			if self.__widgets is None:
				return

			widget = self.__widgets.get_widget('preferences_ymin_entry')
			widget.set_text(str(ymin))

		return locals()

	@Property
	def ymax():
		def fget(self):
			if self.__backend is None:
				return None

			return self.__backend.ymax
				
		def fset(self, ymax):
			if self.__backend is None:
				return

			self.__backend.ymax = ymax

			if self.__widgets is None:
				return

			widget = self.__widgets.get_widget('preferences_ymax_entry')
			widget.set_text(str(ymax))

		return locals()

	def on_saveas_ok_button_clicked(self, widget, data=None):
		self.__saveas.hide()

		filename = self.__saveas.get_filename()
		if filename is None:
			return

		self.saveas(filename, self.__backend.xandys)

	def on_saveas_cancel_button_clicked(self, widget, data=None):
		self.__saveas.hide()

	def on_plot_saveas_button_clicked(self, widget, data=None):
		self.__saveas = self.__widgets.get_widget('saveas_chooser')
		self.__saveas.show()

	def on_saveas_chooser_delete_event(self, widget, data=None):
		self.__saveas.hide()
		return True

	def on_preferences_ok_button_clicked(self, widget, data=None):
		self.__preferences.hide()

		widget = self.__widgets.get_widget('preferences_xmin_entry')
		self.__backend.xmin = float(widget.get_text())

		widget = self.__widgets.get_widget('preferences_xmax_entry')
		self.__backend.xmax = float(widget.get_text())

		widget = self.__widgets.get_widget('preferences_ymin_entry')
		self.__backend.ymin = float(widget.get_text())

		widget = self.__widgets.get_widget('preferences_ymax_entry')
		self.__backend.ymax = float(widget.get_text())

		self.draw()

	def on_preferences_cancel_button_clicked(self, widget, data=None):
		self.__preferences.hide()

	def on_plot_preferences_button_clicked(self, widget, data=None):
		self.__preferences = self.__widgets.get_widget('preferences_dialog')
		self.__preferences.show()

	def on_preferences_dialog_delete_event(self, widget, data=None):
		self.__preferences.hide()
		return True

	def on_plot_overlay_button_toggled(self, widget, data=None):
		self.overlay = widget.get_active()

	def on_plot_window_destroy(self, widget, data=None):
		gtk.main_quit()

	def show(self):
		self.__backend.show()
		self.__container.show()

	def hide(self):
		self.__container.hide()
		self.__backend.hide()

	def run(self):
		gtk.main()

	def plotr(self, *args, **kwargs):
		self.__backend.plotr(*args, **kwargs)

	def plotl(self, *args, **kwargs):
		self.__backend.plotl(*args, **kwargs)

	def ploth(self, *args, **kwargs):
		self.__backend.ploth(*args, **kwargs)

	def plotv(self, *args, **kwargs):
		self.__backend.plotv(*args, **kwargs)

	def draw(self, *args, **kwargs):
		self.__backend.draw(*args, **kwargs)

	def clear(self, *args, **kwargs):
		if self.overlay is True:
			return

		self.__backend.clear(*args, **kwargs)

	def __init__(self, container):
		Common.__init__(self)

		# TODO: this should not be needed, but is required by the glade autoconnect below
		self.__widgets = None
		self.__backend = Backend()

		# TODO: this should not be needed, but is required by the glade autoconnect below
		self.xmin = 0
		self.xmax = 0
		self.ymin = 0
		self.ymax = 0

		gladename = os.environ['GRIMA_ETC'] + '/' + 'grima.glade'
		self.__widgets = gtk.glade.XML(gladename)

		map = {}
		for key in dir(self.__class__):
			map[key] = getattr(self, key)
		self.__widgets.signal_autoconnect(map)

		if container is not None:
			self.__container = container
			widget = self.__widgets.get_widget('plot_embeddable')
			container = self.__widgets.get_widget('plot_container')
			container.remove(widget)
			self.__container.add(widget)
		else:
			self.__container = self.__widgets.get_widget('plot_window')

			# TODO: this should not be needed, but somehow the widget show'ing order
			# is all screwed up and the window doesn't display correctly without this
			self.__container.set_default_size(700, 500)

		widget = self.__widgets.get_widget('plot_backend')
		widget.add(self.__backend.widget)

class Plot(Object):

	@Property
	def xmin():
		def fget(self):
			if self.__display is None:
				return None

			return self.__display.xmin
				
		def fset(self, xmin):
			if self.__display is None:
				return None

			self.__display.xmin = xmin

		return locals()

	@Property
	def xmax():
		def fget(self):
			return self.__display.xmax
				
		def fset(self, xmax):
			self.__display.xmax = xmax

		return locals()

	@Property
	def ymin():
		def fget(self):
			return self.__display.ymin
				
		def fset(self, ymin):
			self.__display.ymin = ymin

		return locals()

	@Property
	def ymax():
		def fget(self):
			return self.__display.ymax
				
		def fset(self, ymax):
			self.__display.ymax = ymax

		return locals()

	@Property
	def overlay():
		def fget(self):
			return self.__display.overlay
				
		def fset(self, overlay):
			self.__display.overlay = overlay

		return locals()

	def __create_display(self):
		try:
			if self.enabled is False:
				return
		except:
			return

		self.__display = None

		try:
			if self.type is 'console':
				self.__display = Console()
			if self.type is 'window':
				self.__display = Window(self.container)

			# TODO: use properties
			self.xmin = 0
			self.xmax = 0
			self.ymin = 0
			self.ymax = 0
			self.overlay = False
		except:
			self.enabled = False

	@Property
	def type():
		def fget(self):
			return self.__type
				
		def fset(self, type):
			self.__type = type
			self.__create_display()

		return locals()

	@Property
	def enabled():
		def fget(self):
			return self.__enabled
				
		def fset(self, enabled):
			self.__enabled = enabled
			self.__create_display()

		return locals()

	def show(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.show(*args, **kwargs)

	def hide(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.hide(*args, **kwargs)

	def run(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.run(*args, **kwargs)

	def plotr(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.plotr(*args, **kwargs)

	def plotl(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.plotl(*args, **kwargs)

	def ploth(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.ploth(*args, **kwargs)

	def plotv(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.plotv(*args, **kwargs)

	def draw(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.draw(*args, **kwargs)

	def clear(self, *args, **kwargs):
		if self.enabled is False:
			return

		self.__display.clear(*args, **kwargs)

	def __init__(self):
		Object.__init__(self)

		self.type = 'console'
		self.container = None
		self.enabled = False

		# TODO: use properties
