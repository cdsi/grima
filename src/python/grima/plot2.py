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

from matplotlib.figure import Figure

# www.gtk.org
import gtk

# our own libraries
from elrond.macros import clamp
from elrond.ui import Widget, Playable, SaveAs
from elrond.util import APINotImplemented, Object, Property

class IBackend(Object):
        """The IBackend class is the base implementation for any class that can produce plots.
        e.g. ASCII art or fancy GUI backends like matplotlib.
        """

        def open(self, filename):
                self.clear()

                with open(filename, 'r') as f:
                        storage = json.load(f)

                print 'File: %s' % (filename)
                print 'Timestamp: %s' % (storage['timestamp'])

                for data in storage['data']:
                        self.plotl(data['x'], data['y'], xlabel=data['xlabel'], ylabel=data['ylabel'],
                                   style=data['style'], color=int(data['color'], 0))

                self.draw()

                if not self.prefs.overlay:
                        self.__storage['data'] = []

                self.__storage['data'].extend(storage['data'])

        def save(self, filename):
                self.__storage['timestamp'] = time.ctime(time.time())

                with open(filename, 'w') as f:
                        json.dump(self.__storage, f, indent=8)

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

        def __init__(self):
                Object.__init__(self)

                self.__storage = {
                        'data': []
                        }

class SubPlot(Playable):

        def __set_limits(self, axes, limits):
                axes.axis('auto')

                if filter(lambda x: x != 0, limits):
                        axes.axis(limits)

        def set_limitsl(self, limits):
                self.__set_limits(self.__axes['axl'], limits)

        def set_limitsr(self, limits):
                self.__set_limits(self.__axes['axr'], limits)

        def __plot__(self, axes, xlabel, ylabel):
                if not self.overlay:
                        self.clear()

                if xlabel:
                        axes.set_xlabel(xlabel)
                if ylabel:
                        axes.set_ylabel(ylabel)

                axes.grid(True)

        def plotl(self, x, y, xlabel=None, ylabel=None, style='-', color=0xFF0000):
                axes = self.__axes['axl']
                self.__plot__(axes, xlabel, ylabel)
                axes.plot(x, y, style, color='#%06X' % (color))

        def plotlh(self, y, xlabel=None, ylabel=None, style='--', color=0xFF0000):
                axes = self.__axes['axl']
                self.__plot__(axes, xlabel, ylabel)
                axes.axhline(y, ls=style, color='#%06X' % (color))

        def plotlv(self, x, xlabel=None, ylabel=None, style='--', color=0xFF0000):
                axes = self.__axes['axl']
                self.__plot__(axes, xlabel, ylabel)
                axes.axvline(x, ls=style, color='#%06X' % (color))

        @APINotImplemented
        def plotr(self, x, y, xlabel=None, ylabel=None, style='-', color=0xFF0000):
                axes = self.__axes['axr']
                self.__plot__(axes, xlabel, ylabel)
                axes.plot(x, y, style, color='#%06X' % (color))

        @APINotImplemented
        def plotrh(self, y, xlabel=None, ylabel=None, style='--', color=0xFF0000):
                axes = self.__axes['axr']
                self.__plot__(axes, xlabel, ylabel)
                axes.axhline(y, ls=style, color='#%06X' % (color))

        @APINotImplemented
        def plotrv(self, x, xlabel=None, ylabel=None, style='--', color=0xFF0000):
                axes = self.__axes['axr']
                self.__plot__(axes, xlabel, ylabel)
                axes.axvline(x, ls=style, color='#%06X' % (color))

        def reset(self, nsubplots, i):
                axl = self.__axes['axl']
                axr = self.__axes['axr']

                axl.grid(True)
                axl.yaxis.set_label_position('left')
                axl.yaxis.tick_left()

                # TODO: axr.grid(True)
                # TODO: axr.yaxis.set_label_position('right')
                # TODO: axr.yaxis.tick_right()

                axl.change_geometry(nsubplots, 1, nsubplots - i)

        def clear(self):
                self.__axes['axl'].clear()
                # TODO: self.__axes['axr'].clear()

        def __play(self):
                while self.is_running:
                        try:
                                with open(self.socket, 'r') as fd:
                                        while self.is_running:
                                                # TODO: readline needs a timeout
                                                line = fd.readline()
                                                if line == '':
                                                        break

                                                gtk.gdk.threads_enter()
                                                self.append(line)
                                                gtk.gdk.threads_leave()

                                                yield
                        except:
                                pass

        def axes_new(self, figure, nsubplots):
                axl = figure.add_subplot(nsubplots + 1, 1, nsubplots + 1)
                axr = None # TODO: axl.twinx()

                self.__axes = {'axl': axl, 'axr': axr}

        def axes_delete(self, figure):
                figure.delaxes(self.__axes['axl'])

        def __init__(self):
                self.overlay = True

class Plot(Widget):

        @Property
        def overlay():
                def fget(self):
                        return self.prefs['overlay'].enabled

                def fset(self, overlay):
                        for subplot in self.__subplots:
                                subplot.overlay = overlay

                        widget = self.builder.get_object('overlay__enabled')
                        widget.set_active(overlay)

                return locals()

        def __reset(self):
                nsubplots = len(self.__subplots)

                for i, subplot in enumerate(self.__subplots):
                        subplot.reset(nsubplots, i)

                self.__figure.subplots_adjust()

        def subplot_new(self):
                subplot = SubPlot()
                subplot.axes_new(self.__figure, len(self.__subplots))

                self.__subplots.append(subplot)
                self.__reset()

                return subplot

        def subplot_delete(self, subplot):
                subplot.axes_delete(self.__figure)

                self.__subplots.remove(subplot)
                self.__reset()

        def __save(self, filename):
                if not filename:
                        return

                self.__filename = filename

                with open(self.__filename, 'w') as fd:
                        fd.write(self.__buffer.get_text(*self.__buffer.get_bounds()))

        def clear(self):
                for subplot in self.__subplots:
                        subplot.clear()

                self.__reset()

                self.__canvas.draw()
                self.draw()

        def show(self):
                self.widget.show()
                self.__canvas.show()
                self.__toolbar.show()

        def hide(self):
                self.__toolbar.hide()
                self.__canvas.hide()
                self.widget.hide()

        def on_open(self, widget):
                pass

        def on_save(self, widget):
                if self.__filename:
                        self.__save(self.__filename)
                else:
                        self.__chooser.get_selection()

        def on_saveas(self, widget):
                self.__chooser.get_selection(filename=self.__filename)

        def on_clear(self, widget):
                self.clear()

        def __init__(self, container=None):
                Widget.__init__(self)

                path = os.environ['GRIMA_ETC']
                name = 'grima-plot2'

                self.loadui(path, name)
                self.loaddb(path, name)

                from matplotlib.backends.backend_gtk \
                  import FigureCanvasGTK as FigureCanvas

                self.__figure = Figure()
                self.__canvas = FigureCanvas(self.__figure)

                from matplotlib.backends.backend_gtk \
                  import NavigationToolbar2GTK as NavigationToolbar

                self.__toolbar = NavigationToolbar(self.__canvas, None)

                widget = gtk.VBox()
                widget.show()

                widget.pack_start(self.__canvas)
                widget.pack_start(self.__toolbar, False, False)

                if not container:
                        container = self.builder.get_object('container')

                container.add(widget)

                self.__filename = None
                self.__subplots = []

                self.__chooser = SaveAs()
                self.__chooser.deletable = False
                self.__chooser.embedded = True
                self.__chooser.callback = self.__save

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
