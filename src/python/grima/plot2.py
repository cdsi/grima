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
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas
from matplotlib.backends.backend_gtkcairo import NavigationToolbar2GTK as NavigationToolbar

# www.gtk.org
import gtk

# our own libraries
from elrond.macros import clamp
from elrond.ui import Widget, Playable, SaveAs
from elrond.util import APINotImplemented, Object, Property

class SubPlot(Widget):

        def __set_limits(self, axes, limits):
                axes.axis('auto')

                if filter(lambda x: x != 0, limits):
                        axes.axis(limits)

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

        def draw(self):
                axl = self.__axes['axl']
                self.__set_limits(axl, self.limitsl)

                # TODO: axr = self.__axes['axr']
                # TODO: self.__set_limits(axr, self.limitsr)

                self.__canvas.draw()

        def axes_new(self, figure, canvas, nsubplots):
                axl = figure.add_subplot(nsubplots + 1, 1, nsubplots + 1)
                axr = None # TODO: axl.twinx()

                self.__axes = {'axl': axl, 'axr': axr}

                self.__canvas = canvas

        def axes_delete(self, figure):
                figure.delaxes(self.__axes['axl'])

        def __init__(self):
                Widget.__init__(self)

                self.limitsl = []
                self.limitsr = []

                self.overlay = True

class StripChart(SubPlot, Playable):

        def __tasklette(self, producer, interval=1, duration=60):
                self.limitsl[0] = 0
                self.limitsl[1] = duration

                x = [0, 0]
                y = [0, 0]

                offset = time.time()

                for data in producer():
                        elapsed = time.time() - offset

                        if elapsed > duration:
                                self.limitsl[0] += elapsed - x[1]
                                self.limitsl[1] += elapsed - x[1]

                        x[1] = elapsed

                        for __y in data:
                                y[1] = __y
                                
                                gtk.gdk.threads_enter()
                                self.plotl(x, y)
                                self.draw()
                                gtk.gdk.threads_leave()

                                y[0] = y[1]

                        x[0] = x[1]

                        time.sleep(interval)

        def __init__(self):
                SubPlot.__init__(self)
                Playable.__init__(self, self.__tasklette)

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

        def __subplot_new(self, subplot):
                subplot.axes_new(self.__figure, self.__canvas, len(self.__subplots))

                self.__subplots.append(subplot)
                self.__reset()

                return subplot

        def __subplot_delete(self, subplot):
                subplot.axes_delete(self.__figure)

                self.__subplots.remove(subplot)
                self.__reset()

        def subplot_new(self):
                return self.__subplot_new(SubPlot())

        def subplot_delete(self, subplot):
                self.__subplot_delete(subplot)

        def stripchart_new(self):
                return self.__subplot_new(StripChart())

        def stripchart_delete(self, stripchart):
                self.__subplot_delete(stripchart)

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

        def __init__(self):
                Widget.__init__(self)

                path = os.environ['GRIMA_ETC']
                name = 'grima-plot2'

                self.loadui(path, name)
                self.loaddb(path, name)

                self.__figure = Figure()
                self.__canvas = FigureCanvas(self.__figure)
                self.__toolbar = NavigationToolbar(self.__canvas, None)

                widget = gtk.VBox()
                widget.show()

                widget.pack_start(self.__canvas)
                widget.pack_start(self.__toolbar, False, False)

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
