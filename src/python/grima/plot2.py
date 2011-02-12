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
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

from mpl_toolkits.mplot3d import Axes3D

# www.gtk.org
import gtk

# our own libraries
from elrond.static import *
from elrond.ui import Widget, Playable, SaveAs
from elrond.util import APINotImplemented, Object, Property

class SubPlot(Widget):

        @Property
        def axl():
                def fget(self):
                        return self.__axes['axl']

                def fset(self, value):
                        pass

                return locals()

        @Property
        def axr():
                def fget(self):
                        return self.__axes['axr']

                def fset(self, value):
                        pass

                return locals()

        def __set_title(self, axes, title):
                if title:
                        axes.set_title(title)

        def __set_limits(self, axes, xlimits, ylimits):
                axes.axis('auto')

                if xlimits[0] or xlimits[1]:
                        axes.set_xlim(xlimits)
                if ylimits[0] or ylimits[1]:
                        axes.set_ylim(ylimits)

        def __set_labels(self, axes, xlabel, ylabel):
                if xlabel:
                        axes.set_xlabel(xlabel)
                if ylabel:
                        axes.set_ylabel(ylabel)

        def __plot__(self, axes, xlabel, ylabel):
                if not self.overlay:
                        self.clear()

                self.__set_labels(axes, xlabel, ylabel)

                axes.grid(True)

        def plotl(self, x, y, xlabel=None, ylabel=None, style='-', color=0xFF0000,\
		  mec='r', mfc='None', mew=1, ms=6, linewidth=1, label=None, picker=None):
                axes = self.__axes['axl']
                self.__plot__(axes, xlabel, ylabel)

                pl = axes.plot(x, y, style, color='#%06X' % (color), mec=mec,
                                mfc=mfc, mew=mew, ms=ms, linewidth=linewidth, label=label, picker=picker)

        def plotlh(self, y, xlabel=None, ylabel=None, style='--', color=0xFF0000):
                axes = self.__axes['axl']
                self.__plot__(axes, xlabel, ylabel)
                axes.axhline(y, ls=style, color='#%06X' % (color))

        def plotlv(self, x, xlabel=None, ylabel=None, style='--', color=0xFF0000):
                axes = self.__axes['axl']
                self.__plot__(axes, xlabel, ylabel)
                axes.axvline(x, ls=style, color='#%06X' % (color))

        def text(self, x, y, s, fontsize=12, backgroundcolor='w', va='bottom', ha='left', transform=False):
                axes=self.__axes['axl']

                if transform:
                        axes.text(x, y, s, fontsize=fontsize, backgroundcolor=backgroundcolor, \
                                  va=va, ha=ha, transform = axes.transAxes)
                else:
                        axes.text(x, y, s, fontsize=fontsize, backgroundcolor=backgroundcolor, \
                                  va=va, ha=ha)

        def grid(self, grid):
                axes=self.__axes['axl']
                axes.grid(grid)

        def annotate(self, text, xy, family, va):
                axes=self.__axes['axl']
                axes.annotate(text, xy, family=family, va=va)

        def blankticks(self):
                axes = self.__axes['axl']
                axes.set_xticklabels([], visible=False)
                axes.set_yticklabels([], visible=False)

        def addcollection(self, collection):
                axes = self.__axes['axl']
                axes.add_collection(collection)

        def get_limits(self):
                axes = self.__axes['axl']
                return axes.get_xlim() + axes.get_ylim()

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
                self.__set_limits(axl, self.xlimitsl, self.ylimitsl)
                self.__set_labels(axl, self.xlabel, self.ylabel)
                self.__set_title(axl, self.title)

                # TODO: axr = self.__axes['axr']
                # TODO: self.__set_limits(axr, self.xlimitsr, self.ylimitsr)
                # TODO: self.__set_labels(axr, self.xlabel, self.ylabel)

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

                self.title = None

                self.xlimitsl = [0, 0]
                self.xlimitsr = [0, 0]
                self.ylimitsl = [0, 0]
                self.ylimitsr = [0, 0]

                self.xlabel = ''
                self.ylabel = ''

                self.overlay = True

class StripChart(SubPlot, Playable):

        def __tasklette(self, producer, interval=1, duration=60):
                self.xlimitsl[0] = 0
                self.xlimitsl[1] = duration

                x = [0, 0]
                y = [0, 0]

                offset = time.time()

                for data in producer():
                        elapsed = time.time() - offset

                        if elapsed > duration:
                                self.xlimitsl[0] += elapsed - x[1]
                                self.xlimitsl[1] += elapsed - x[1]

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
                        for plotable in self.__plotables:
                                plotable.overlay = overlay

                        widget = self.builder.get_object('overlay__enabled')
                        widget.set_active(overlay)

                return locals()

        @Property
        def canvas():
                def fget(self):
                        return self.__canvas

                return locals()

        @Property
        def toolbar():
                def fget(self):
                        return self.__toolbar

                return locals()

        def __reset(self):
                nplotables = len(self.__plotables)

                for i, plotable in enumerate(self.__plotables):
                        plotable.reset(nplotables, i)

                self.__figure.subplots_adjust(hspace = 0.5)

        def __plotable_new(self, plotable):
                plotable.axes_new(self.__figure, self.__canvas, len(self.__plotables))

                self.__plotables.append(plotable)
                self.__reset()

                return plotable

        def __plotable_delete(self, plotable):
                plotable.axes_delete(self.__figure)

                self.__plotables.remove(plotable)
                self.__reset()

        def subplot_new(self):
                return self.__plotable_new(SubPlot())

        def subplot_delete(self, plotable):
                self.__plotable_delete(plotable)

        def stripchart_new(self):
                return self.__plotable_new(StripChart())

        def stripchart_delete(self, stripchart):
                self.__plotable_delete(stripchart)

        def plot3d_new(self):
                return self.__plotable_new(Plot3D())

        def plot3d_delete(self, plot3d):
                self.__plotable_delete(plot3d)

        def __save(self, filename):
                if not filename:
                        return

                self.__filename = filename

                with open(self.__filename, 'w') as fd:
                        fd.write(self.__buffer.get_text(*self.__buffer.get_bounds()))

        def clear(self):
                for plotable in self.__plotables:
                        plotable.clear()

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
                self.__plotables = []

                self.__chooser = SaveAs()
                self.__chooser.deletable = False
                self.__chooser.embedded = True
                self.__chooser.callback = self.__save

class Plot3D(SubPlot):

        def axes_new(self, figure, canvas, nsubplots):
                axl = Axes3D(figure)
                axr = None # TODO: axl.twinx()

                self.__axes = {'axl': axl, 'axr': axr}

                self.__canvas = canvas

        def reset(self, nsubplots, i):
                axl = self.__axes['axl']
                axr = self.__axes['axr']

                axl.grid(True)
                axl.yaxis.set_label_position('left')
                axl.yaxis.tick_left()

        def draw(self):
                self.__canvas.draw()

        def plotl(self, x, y, z, xlabel=None, ylabel=None, label=None):
                axes = self.__axes['axl']
                self.__plot__(axes, xlabel, ylabel)
                axes.plot(x, y, z, label=label)
                try:
                        axes.legend(numpoints=1)
                except:
                        pass

        def __init__(self):
                SubPlot.__init__(self)

                self.zlimitsl = [0, 0]
                self.zlimitsr = [0, 0]

                self.zlabel = ''

class Cursor:
        def __init__(self, ax, plot):
                self.ax = ax
                self.canvas = plot.canvas

                self.plot = plot

                self.lx = self.ax.axhline(color='r', linewidth=2)
                self.ly = self.ax.axvline(color='r', linewidth=2)

                self.hide()

                self.txt = ax.text(0.7, 0.9, '', transform=self.ax.transAxes)

                self.txt.set_visible(False)

                self.background = self.canvas.copy_from_bbox(self.ax.bbox)

                self.canvas.mpl_connect('draw_event', self.on_draw)
                self.canvas.mpl_connect('motion_notify_event', self.on_motion)

                self.restricted = False

        def show(self):
                self.lx.set_visible(True)
                self.ly.set_visible(True)

        def hide(self):
                self.lx.set_visible(False)
                self.ly.set_visible(False)

        def restrict(self, value):
                self.restricted = value

        def on_draw(self, event):
                self.hide()
                self.ax.draw_artist(self.ax)
                self.background = self.canvas.copy_from_bbox(self.ax.bbox)

        def on_motion(self, event):
                if self.restricted:
                        return

                if not event.inaxes:
                        self.hide()
                        self.canvas.restore_region(self.background)
                        self.canvas.blit(self.ax.bbox)
                        return

                self.show()

                self.canvas.restore_region(self.background)

                x, y = event.xdata, event.ydata

                self.lx.set_ydata(y)
                self.ly.set_xdata(x)

                self.txt.set_text('x=%1.2f, y=%1.2f' % (x,y))

                self.ax.draw_artist(self.lx)
                self.ax.draw_artist(self.ly)
                self.ax.draw_artist(self.txt)

                self.canvas.blit(self.ax.bbox)

class SnapCursor(Cursor):
        def __init__(self, ax, plot, x, y):
                Cursor.__init__(self, ax, plot)

                self.x = x
                self.z = zip(x,y)

                self.x.sort()
                self.z.sort()

        def on_motion(self, event):
                if self.hidden or not event.inaxes:
                        return

                self.canvas.restore_region(self.background)

                x, y = event.xdata, event.ydata

                i = np.searchsorted(self.x, x)

                x, y = self.z[i]

                self.lx.set_ydata(y)
                self.ly.set_xdata(x)

                self.txt.set_text('x=%1.2f, y=%1.2f' % (x,y))

                self.ax.draw_artist(self.lx)
                self.ax.draw_artist(self.ly)
                self.ax.draw_artist(self.txt)

                self.canvas.blit(self.ax.bbox)

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
