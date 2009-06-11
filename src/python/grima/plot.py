from __future__ import division
from __future__ import with_statement

# standard python libraries
try:
        import json
except:
        import simplejson as json

import re
import os
import time

# matplotlib.sf.net
import matplotlib
import numpy

# www.gtk.org
import gtk

# our own libraries
from elrond.macros import clamp
from elrond.util import Object, Property

def parse(f):
        x = []
        y = []

        fd = open(f, 'r')
        lines = [l.strip() for l in fd.readlines()]
        fd.close()

        for i, line in enumerate(lines):
                data = filter(lambda x: x != '', re.split('[, ]', line.strip()))

                try:
                        y.append(float(data[1]))
                        x.append(float(data[0]))
                except IndexError:
                        y.append(float(data[0]))
                        x.append(i)

        return x, y

##
## Backends...
##

class IBackend(Object):
        """The IBackend class is the base implementation for any class that can produce plots.
        e.g. ASCII art or fancy GUI backends like matplotlib.
        """

        def stripchart(self, filename):
                x_list, y_list = parse(filename)

                self.clear()

                self.props.ymin = 0
                self.props.ymax = 100

                step = 100

                x_first = x_list[0: clamp(step, u=len(x_list))]
                y_first = y_list[0: clamp(step, u=len(y_list))]

                self.props.xmin = 0
                self.props.xmax = len(x_first)

                for i in range(0, len(x_first)):
                        self.plotl(x_first[0:i + 1], y_first[0:i + 1])
                        self.draw()

                self.plotl(x_list, y_list)

                for i in range(0, len(x_list)):
                        self.props.xmin = i + 1
                        self.props.xmax = i + 1 + step

                        self.draw()

        def open(self, filename):
                self.clear()

                if self.subplotkludge:
                        self.subplot_new()

                self.subplotkludge = True

                with open(filename, 'r') as f:
                        storage = json.load(f)

                        print 'File: %s' % (filename)
                        print 'Timestamp: %s' % (storage['timestamp'])

                        for data in storage['data']:
                                self.plotl(data['x'], data['y'], xlabel=data['xlabel'], ylabel=data['ylabel'],
                                           style=data['style'], color=int(data['color'], 0))

                self.draw()

                if not self.props.overlay:
                        self.__storage['data'] = []

                self.__storage['data'].extend(storage['data'])

        def save(self, filename):
                self.__storage['timestamp'] = time.ctime(time.time())

                with open(filename, 'w') as f:
                        json.dump(self.__storage, f, indent=8)

        # TODO:
        def stats(self, x, y):
                print '  len =', len(y)
                print ' mean =', numpy.mean(y)
                print '  sum =', sum(y)
                print '  std =', numpy.std(y)

                ymin = numpy.min(y)
                print ' ymin =', ymin
                print ' xmin =', x[y.index(ymin)]

                ymax = numpy.max(y)
                print ' ymax =', ymax
                print ' xmax =', x[y.index(ymax)]

        def __plot__(self, x, y, style=None, color=0xFF0000, xlabel=None, ylabel=None):
                self.stats(x, y)

                data = {
                        'xlabel': xlabel,
                        'x': x,
                        'ylabel': ylabel,
                        'y': y,
                        'style': style,
                        'color': '0x%06X' % (color)
                }

                if not self.props.overlay:
                        self.__storage['data'] = []

                self.__storage['data'].append(data)

        def plotr(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def plotl(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def ploth(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def plotv(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def draw(self, *args, **kwargs):
                pass

        def clear(self, *args, **kwargs):
                pass

        def show(self, *args, **kwargs):
                pass

        def hide(self, *args, **kwargs):
                pass

        def run(self, *args, **kwargs):
                pass

        def __init__(self):
                Object.__init__(self)

                self.__storage = {
                        'data': []
                }

class ConsoleBackend(IBackend):
        """This is the simplest of backends. This simply prints to the console. This backend
        must be used within a ConsoleContainer.
        """

        def __plot__(self, x, y, style=None, color=0xFF0000, xlabel=None, ylabel=None):
                IBackend.__plot__(self, x, y, style=style, color=color, xlabel=xlabel, ylabel=ylabel)

                for i in range(0, len(x)):
                        print 'x,y[%d] = %.4f, %4f' % (i, x[i], y[i])

class IMatplotlibBackend(IBackend):
        """This backend uses matplotlib to prodce plots. An ImageContainer or WindowContainer in-turn
        contains this backed to either render the plot to and image or to a GUI.
        """

        def __plot__(self, x, y, style='-', color=0xFF0000, xlabel=None, ylabel=None):
                IBackend.__plot__(self, x, y, style=style, color=color, xlabel=xlabel, ylabel=ylabel)

                if xlabel != None:
                        # TODO: self.__axes.set_xlabel(xlabel)
                        pass
                if ylabel != None:
                        # TODO: self.__axes.set_ylabel(ylabel)
                        pass

                self.__axes.plot(x, y, style, color='#%06X' % (color))
                self.__axes.grid(True)

        def plotr(self, *args, **kwargs):
                self.figure.sca(self.__axr)
                if not kwargs.has_key('color'):
                        kwargs['color'] = 0x00FF00
                self.__axes = self.__axr
                self.__plot__(*args, **kwargs)

        def plotl(self, *args, **kwargs):
                self.figure.sca(self.__axl)
                if not kwargs.has_key('color'):
                        kwargs['color'] = 0xFF0000
                self.__axes = self.__axl
                self.__plot__(*args, **kwargs)

        def ploth(self, y, style='--', color=0xFF0000):
                self.__subplot.axhline(y, ls=style, color='#%06X' % (color))
                self.__subplot.grid(True)

        def plotv(self, x, style='--', color=0xFF0000):
                self.__subplot.axvline(x, ls=style, color='#%06X' % (color))
                self.__subplot.grid(True)

        def draw(self):
                limits = [self.props.xmin, self.props.xmax, self.props.yminl, self.props.ymaxl]

                self.__axl.axis('auto')
                if filter(lambda x: x != 0, limits):
                        self.__axl.axis(limits)

                limits = [self.props.xmin, self.props.xmax, self.props.yminr, self.props.ymaxr]

                self.__axr.axis('auto')
                if filter(lambda x: x != 0, limits):
                        self.__axr.axis(limits)

                self.canvas.draw()

        def __reset(self):
                self.__axl.grid(True)
                self.__axl.yaxis.set_label_position('left')
                self.__axl.yaxis.tick_left()

                self.__axr.grid(True)
                self.__axr.yaxis.set_label_position('right')
                self.__axr.yaxis.tick_right()

        def clear(self):
                if not self.props.overlay:
                        self.__axl.clear()
                        self.__axr.clear()

                self.__reset()

        def subplot_new(self):
                nsubplots = len(self.__subplots) + 1

                subplot = self.figure.add_subplot(nsubplots, 1, nsubplots)
                subplot.grid(True)

                self.__subplots.append(subplot)
                self.__subplot = subplot

                for i, subplot in enumerate(self.__subplots):
                        subplot.change_geometry(nsubplots, 1, i + 1)

        def __init__(self):
                IBackend.__init__(self)

                from matplotlib.figure import Figure
                self.figure = Figure()

                self.__subplots = []
                self.subplot_new()

                self.subplotkludge = False

                self.__axl = self.figure.gca()
                self.__axr = self.__axl.twinx()

                self.__reset()

class MatplotlibImageBackend(IMatplotlibBackend):

        def render(self, filename):
                self.figure.savefig(filename)

        def __init__(self):
                IMatplotlibBackend.__init__(self)

                from matplotlib.backends.backend_cairo \
                  import FigureCanvasCairo as FigureCanvas

                self.canvas = FigureCanvas(self.figure)

class MatplotlibWindowBackend(IMatplotlibBackend):

        @Property
        def widget():
                def fget(self):
                        self.__widget = gtk.VBox()

                        self.__widget.pack_start(self.canvas)
                        self.__widget.pack_start(self.toolbar, False, False)

                        return self.__widget

                def fset(self, widget):
                        self.__widget = widget

                return locals()

        def show(self):
                self.__widget.show()
                self.canvas.show()
                self.toolbar.show()

        def hide(self):
                self.toolbar.hide()
                self.canvas.hide()
                self.__widget.hide()

        def __init__(self):
                IMatplotlibBackend.__init__(self)

                from matplotlib.backends.backend_gtk \
                  import FigureCanvasGTK as FigureCanvas

                self.canvas = FigureCanvas(self.figure)

                from matplotlib.backends.backend_gtk \
                  import NavigationToolbar2GTK as NavigationToolbar

                self.toolbar = NavigationToolbar(self.canvas, None)

##
## Containers...
##

class IContainer(Object):
        """The IContainer class is the base implementation for any class that contains IBackends.
        e.g. console wrappers, image only wrappers, or fancy GUI toolkits like GTK+.
        """

        @Property
        def props():
                def fget(self):
                        return self.backend.props

                def fset(self, props):
                        self.backend.props = props

                return locals()

        def plotr(self, *args, **kwargs):
                self.backend.plotr(*args, **kwargs)

        def plotl(self, *args, **kwargs):
                self.backend.plotl(*args, **kwargs)

        def ploth(self, *args, **kwargs):
                self.backend.ploth(*args, **kwargs)

        def plotv(self, *args, **kwargs):
                self.backend.plotv(*args, **kwargs)

        def draw(self, *args, **kwargs):
                self.backend.draw(*args, **kwargs)

        def clear(self, *args, **kwargs):
                self.backend.clear(*args, **kwargs)

        def show(self, *args, **kwargs):
                self.backend.show(*args, **kwargs)

        def hide(self, *args, **kwargs):
                self.backend.hide(*args, **kwargs)

        def run(self, *args, **kwargs):
                self.backend.run(*args, **kwargs)

        def stripchart(self, filename):
                self.backend.stripchart(filename)

        def open(self, filename):
                self.backend.open(filename)

        def save(self, filename):
                self.backend.save(filename)

class ConsoleContainer(IContainer):

        def __init__(self):
                IContainer.__init__(self)

                self.backend = ConsoleBackend()

class ImageContainer(IContainer):

        def draw(self, *args, **kwargs):
                IContainer.draw(self, *args, **kwargs)

                self.backend.render('foobar.png')

        def __init__(self):
                IContainer.__init__(self)

                self.backend = MatplotlibImageBackend()

class WindowContainer(IContainer):

        @Property
        def props():
                def fget(self):
                        return self.backend.props

                def fset(self, props):
                        self.backend.props = props

                        widget = self.__builder.get_object('preferences_xmin_entry')
                        widget.set_text(str(self.backend.props.xmin))

                        widget = self.__builder.get_object('preferences_xmax_entry')
                        widget.set_text(str(self.backend.props.xmax))

                        widget = self.__builder.get_object('preferences_yminl_entry')
                        widget.set_text(str(self.backend.props.yminl))

                        widget = self.__builder.get_object('preferences_ymaxl_entry')
                        widget.set_text(str(self.backend.props.ymaxl))

                        widget = self.__builder.get_object('preferences_yminr_entry')
                        widget.set_text(str(self.backend.props.yminr))

                        widget = self.__builder.get_object('preferences_ymaxr_entry')
                        widget.set_text(str(self.backend.props.ymaxr))

                return locals()

        @Property
        def title():
                def fget(self):
                        return self.__title

                def fset(self, title):
                        self.__title = title

                        if not self.__title:
                                return

                        self.__container.set_title(self.__title)

                return locals()

        def clear(self, *args, **kwargs):
                IContainer.clear(self, *args, **kwargs)

        def show(self, *args, **kwargs):
                IContainer.show(self, *args, **kwargs)

                self.__container.show()

        def hide(self, *args, **kwargs):
                IContainer.hide(self, *args, **kwargs)

                self.__container.hide()

        def run(self):
                gtk.main()

        def on_open_ok_button_clicked(self, widget, data=None):
                self.__open.hide()

                filename = self.__open.get_filename()
                if not filename:
                        return
                self.__open.set_filename(filename)

                self.open(filename)

        def on_open_cancel_button_clicked(self, widget, data=None):
                self.__open.hide()

        def on_open_chooser_delete_event(self, widget, data=None):
                self.__open.hide()
                return True

        def on_plot_open_button_clicked(self, widget, data=None):
                self.__open = self.__builder.get_object('open_chooser')
                self.__open.show()

        def on_plot_save_button_clicked(self, widget, data=None):
                if not self.filename:
                        self.on_plot_saveas_button_clicked(self, None)

                if self.filename:
                        self.save(self.filename)

        def on_saveas_ok_button_clicked(self, widget, data=None):
                self.__saveas.hide()

                filename = self.__saveas.get_filename()
                if not filename:
                        return
                self.__saveas.set_filename(filename)

                self.filename = filename

                self.on_plot_save_button_clicked(self, None)

        def on_saveas_cancel_button_clicked(self, widget, data=None):
                self.__saveas.hide()

        def on_saveas_chooser_delete_event(self, widget, data=None):
                self.__saveas.hide()
                return True

        def on_plot_saveas_button_clicked(self, widget, data=None):
                self.__saveas = self.__builder.get_object('saveas_chooser')
                self.__saveas.show()

        def on_preferences_ok_button_clicked(self, widget, data=None):
                self.__preferences.hide()

                widget = self.__builder.get_object('preferences_xmin_entry')
                self.props.xmin = float(widget.get_text())

                widget = self.__builder.get_object('preferences_xmax_entry')
                self.props.xmax = float(widget.get_text())

                widget = self.__builder.get_object('preferences_yminl_entry')
                self.props.yminl = float(widget.get_text())

                widget = self.__builder.get_object('preferences_ymaxl_entry')
                self.props.ymaxl = float(widget.get_text())

                widget = self.__builder.get_object('preferences_yminr_entry')
                self.props.yminr = float(widget.get_text())

                widget = self.__builder.get_object('preferences_ymaxr_entry')
                self.props.ymaxr = float(widget.get_text())

                self.draw()

        def on_preferences_cancel_button_clicked(self, widget, data=None):
                self.__preferences.hide()

        def on_plot_preferences_button_clicked(self, widget, data=None):
                self.__preferences = self.__builder.get_object('preferences_dialog')
                self.__preferences.show()

        def on_preferences_dialog_delete_event(self, widget, data=None):
                self.__preferences.hide()
                return True

        def on_plot_overlay_button_toggled(self, widget, data=None):
                self.props.overlay = widget.get_active()

        def on_plot_window_destroy(self, widget, data=None):
                gtk.main_quit()

        def __init__(self, container):
                IContainer.__init__(self)

                self.backend = MatplotlibWindowBackend()

                buildername = os.environ['GRIMA_ETC'] + os.sep + 'grima-plot.ui'
                self.__builder = gtk.Builder()
                self.__builder.add_from_file(buildername)
                self.__builder.connect_signals(self)

                if container:
                        self.__container = container
                        widget = self.__builder.get_object('plot_embeddable')
                        container = self.__builder.get_object('plot_container')
                        container.remove(widget)
                        self.__container.add(widget)
                else:
                        self.__container = self.__builder.get_object('plot_window')

                        # TODO: this should not be needed, but somehow the widget show'ing order
                        # is all screwed up and the window doesn't display correctly without this
                        self.__container.set_default_size(700, 500)

                widget = self.__builder.get_object('plot_backend')
                widget.add(self.backend.widget)

                # TODO:
                self.filename = None

##
## This is the public API...
##

class Plot(Object):

        def __create_display(self):
                if not self.__enabled:
                        return

                if self.type == 'console':
                        self.__display = ConsoleContainer()
                if self.type == 'image':
                        self.__display = ImageContainer()
                if self.type == 'window':
                        self.__display = WindowContainer(self.container)

                try:
                        self.__display.props = self
                        self.__display.title = self.title
                except:
                        self.__enabled = False

        @Property
        def enabled():
                def fget(self):
                        return self.__enabled

                def fset(self, enabled):
                        self.__enabled = enabled
                        self.__create_display()

                return locals()

        @Property
        def type():
                def fget(self):
                        return self.__type

                def fset(self, type):
                        self.__type = type
                        self.__create_display()

                return locals()

        @Property
        def title():
                def fget(self):
                        return self.__title

                def fset(self, title):
                        self.__title = title

                return locals()

        def plotr(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.plotr(*args, **kwargs)

        def plotl(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.plotl(*args, **kwargs)

        def ploth(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.ploth(*args, **kwargs)

        def plotv(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.plotv(*args, **kwargs)

        def draw(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.draw(*args, **kwargs)

        def clear(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.clear(*args, **kwargs)

        def show(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.show(*args, **kwargs)

        def hide(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.hide(*args, **kwargs)

        def run(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.run(*args, **kwargs)

        def stripchart(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.stripchart(*args, **kwargs)

        def open(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.open(*args, **kwargs)

        def save(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.save(*args, **kwargs)

        def __init__(self):
                Object.__init__(self)

                self.enabled = False
                self.container = None
                self.type = 'console'
                self.title = None

                # TODO: use preferences
                self.xmin = 0
                self.xmax = 0
                self.yminl = 0
                self.ymaxl = 0
                self.yminr = 0
                self.ymaxr = 0
                self.overlay = False

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
