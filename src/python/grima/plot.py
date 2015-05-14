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
from elrond.static import *
from elrond.util import APINotImplemented, Object, Property

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

                self.prefs.ymin = 0
                self.prefs.ymax = 100

                step = 100

                x_first = x_list[0: clamp(step, u=len(x_list))]
                y_first = y_list[0: clamp(step, u=len(y_list))]

                self.prefs.xmin = 0
                self.prefs.xmax = len(x_first)

                for i in range(0, len(x_first)):
                        self.plotl(x_first[0:i + 1], y_first[0:i + 1])
                        self.draw()

                self.plotl(x_list, y_list)

                for i in range(0, len(x_list)):
                        self.prefs.xmin = i + 1
                        self.prefs.xmax = i + 1 + step

                        self.draw()

        def open(self, filename, i=None):
                self.clear()

                with open(filename, 'r') as f:
                        storage = json.load(f)

                print 'File: %s' % (filename)
                print 'Timestamp: %s' % (storage['timestamp'])

                for data in storage['data']:
                        self.plotl(data['x'], data['y'], i=i, xlabel=data['xlabel'], ylabel=data['ylabel'],
                                   style=data['style'], color=int(data['color'], 0))

                self.draw()

                if not self.prefs.overlay:
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

                if not self.prefs.overlay:
                        self.__storage['data'] = []

                self.__storage['data'].append(data)

        def plotr(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def plotl(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def plotlh(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def plotlv(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def plotrh(self, *args, **kwargs):
                self.__plot__(*args, **kwargs)

        def plotrv(self, *args, **kwargs):
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

        def __plot__(self, x, y, i=None, axes=None, style='-', color=0xFF0000, xlabel=None, ylabel=None):
                IBackend.__plot__(self, x, y, style=style, color=color, xlabel=xlabel, ylabel=ylabel)

                if i is None or axes is None:
                        # TODO: raise an exception
                        return

                if not xlabel is None:
                        # TODO: axes.set_xlabel(xlabel)
                        pass
                if not ylabel is None:
                        # TODO: axes.set_ylabel(ylabel)
                        pass

                if i > self.__nsubplots - 1:
                        self.subplot_new()

                subplot = self.__subplots[i][axes]

                subplot.plot(x, y, style, color='#%06X' % (color))
                subplot.grid(True)

        def plotl(self, *args, **kwargs):
                if not 'i' in kwargs:
                        kwargs['i'] = self.__isubplot
                kwargs['axes'] = 'axl'
                self.__plot__(*args, **kwargs)

        @APINotImplemented
        def plotr(self, *args, **kwargs):
                if not 'i' in kwargs:
                        kwargs['i'] = self.__isubplot
                kwargs['axes'] = 'axr'
                self.__plot__(*args, **kwargs)

        def plotlh(self, y, i=None, style='--', color=0xFF0000):
                # TODO: must call self.__plot__
                if i is None:
                        i = self.__isubplot
                self.__subplots[i]['axl'].axhline(y, ls=style, color='#%06X' % (color))
                self.__subplots[i]['axl'].grid(True)

        def plotlv(self, x, i=None, style='--', color=0xFF0000):
                # TODO: must call self.__plot__
                if i is None:
                        i = self.__isubplot
                self.__subplots[i]['axl'].axvline(x, ls=style, color='#%06X' % (color))
                self.__subplots[i]['axl'].grid(True)

        @APINotImplemented
        def plotrh(self, y, i=None, style='--', color=0xFF0000):
                # TODO: must call self.__plot__
                if i is None:
                        i = self.__isubplot
                self.__subplots[i]['axr'].axhline(y, ls=style, color='#%06X' % (color))
                self.__subplots[i]['axr'].grid(True)

        @APINotImplemented
        def plotrv(self, x, i=None, style='--', color=0xFF0000):
                # TODO: must call self.__plot__
                if i is None:
                        i = self.__isubplot
                self.__subplots[i]['axr'].axvline(x, ls=style, color='#%06X' % (color))
                self.__subplots[i]['axr'].grid(True)

        def __draw(self, subplot, limits):
                subplot.axis('auto')
                if filter(lambda x: x != 0, limits):
                        subplot.axis(limits)

        def draw(self):
                limits = [self.prefs.xmin, self.prefs.xmax, self.prefs.yminl, self.prefs.ymaxl]
                for i, subplot in enumerate(self.__subplots):
                        if i > 0:
                                self.__draw(subplot['axl'], limits)

                # limits = [self.prefs.xmin, self.prefs.xmax, self.prefs.yminr, self.prefs.ymaxr]
                # for i, subplot in enumerate(self.__subplots):
                #         if i > 0:
                #                 self.__draw(subplot['axr'], limits)

                self.canvas.draw()

        def __reset(self):
                for i, subplot in enumerate(self.__subplots):
                        axl = subplot['axl']
                        axr = subplot['axr']

                        axl.grid(True)
                        axl.yaxis.set_label_position('left')
                        axl.yaxis.tick_left()

                        # axr.grid(True)
                        # axr.yaxis.set_label_position('right')
                        # axr.yaxis.tick_right()

                        axl.change_geometry(self.__nsubplots, 1, self.__nsubplots - i)

                self.figure.subplots_adjust()

        def clear(self):
                if not self.prefs.overlay:
                        for subplot in self.__subplots:
                                try:
                                        subplot['axl'].clear()
                                        subplot['axr'].clear()
                                except:
                                        pass

                self.__reset()

        def subplot_new(self):
                self.__isubplot = len(self.__subplots)
                self.__nsubplots = self.__isubplot + 1

                axl = self.figure.add_subplot(self.__nsubplots, 1, self.__nsubplots)
                axr = None # axl.twinx()

                self.__subplots.append({'axl': axl, 'axr': axr})

                self.__reset()

        def get_axes(self):
                return self.__subplots

        def __init__(self):
                IBackend.__init__(self)

                from matplotlib.figure import Figure
                self.figure = Figure()

                self.__subplots = []
                self.subplot_new()

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
        def prefs():
                def fget(self):
                        return self.backend.prefs

                def fset(self, prefs):
                        self.backend.prefs = prefs

                return locals()

        def plotr(self, *args, **kwargs):
                self.backend.plotr(*args, **kwargs)

        def plotl(self, *args, **kwargs):
                self.backend.plotl(*args, **kwargs)

        def plotlh(self, *args, **kwargs):
                self.backend.plotlh(*args, **kwargs)

        def plotlv(self, *args, **kwargs):
                self.backend.plotlv(*args, **kwargs)

        def plotrh(self, *args, **kwargs):
                self.backend.plotrh(*args, **kwargs)

        def plotrv(self, *args, **kwargs):
                self.backend.plotrv(*args, **kwargs)

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

        def stripchart(self, *args, **kwargs):
                self.backend.stripchart(*args, **kwargs)

        def open(self, *args, **kwargs):
                self.backend.open(*args, **kwargs)

        def save(self, *args, **kwargs):
                self.backend.save(*args, **kwargs)

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
        def prefs():
                def fget(self):
                        return self.backend.prefs

                def fset(self, prefs):
                        self.backend.prefs = prefs

                        widget = self.__builder.get_object('preferences_xmin_entry')
                        widget.set_text(str(self.backend.prefs.xmin))

                        widget = self.__builder.get_object('preferences_xmax_entry')
                        widget.set_text(str(self.backend.prefs.xmax))

                        widget = self.__builder.get_object('preferences_yminl_entry')
                        widget.set_text(str(self.backend.prefs.yminl))

                        widget = self.__builder.get_object('preferences_ymaxl_entry')
                        widget.set_text(str(self.backend.prefs.ymaxl))

                        widget = self.__builder.get_object('preferences_yminr_entry')
                        widget.set_text(str(self.backend.prefs.yminr))

                        widget = self.__builder.get_object('preferences_ymaxr_entry')
                        widget.set_text(str(self.backend.prefs.ymaxr))

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
                self.prefs.xmin = float(widget.get_text())

                widget = self.__builder.get_object('preferences_xmax_entry')
                self.prefs.xmax = float(widget.get_text())

                widget = self.__builder.get_object('preferences_yminl_entry')
                self.prefs.yminl = float(widget.get_text())

                widget = self.__builder.get_object('preferences_ymaxl_entry')
                self.prefs.ymaxl = float(widget.get_text())

                widget = self.__builder.get_object('preferences_yminr_entry')
                self.prefs.yminr = float(widget.get_text())

                widget = self.__builder.get_object('preferences_ymaxr_entry')
                self.prefs.ymaxr = float(widget.get_text())

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
                self.prefs.overlay = widget.get_active()

        def on_plot_window_destroy(self, widget, data=None):
                gtk.main_quit()

        def get_axes(self):
                return self.backend.get_axes()

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

                self.__display = None

                if self.type == 'console':
                        self.__display = ConsoleContainer()
                if self.type == 'image':
                        self.__display = ImageContainer()
                if self.type == 'window':
                        self.__display = WindowContainer(self.container)

                try:
                        self.__display.prefs = self
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

                def fset(self, tipe):
                        self.__type = tipe
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

        def plotlh(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.plotlh(*args, **kwargs)

        def plotlv(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.plotlv(*args, **kwargs)

        def plotrh(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.plotrh(*args, **kwargs)

        def plotrv(self, *args, **kwargs):
                if not self.enabled:
                        return

                self.__display.plotrv(*args, **kwargs)

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

        def get_axes(self):
                return self.__display.get_axes()

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
