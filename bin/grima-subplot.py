from __future__ import division
from __future__ import with_statement

from optparse import OptionParser

import numpy as np

import elrond.widgets
import grima.widgets

from grima.plot2 import PlotApp

op = OptionParser('%prog [options] data1 data2 data3 ...')

op.add_option('--title', action='store', dest='title', default=None,
              help='The plot window title.')
op.add_option('--deletable', action='store', dest='deletable', default=True,
              help='When disabled the plot window is not closable.')

(options, args) = op.parse_args()

app = PlotApp()
app.title = options.title
app.deletable = options.deletable

plot = app.get_subwidget('grima-subplot-widget')
plot.overlay = True

x = np.arange(0, 3, .02)
y = np.exp(x)
z = y[::-1]

subplot1 = plot.subplot_new()
plot.subplot_delete(subplot1)

subplot2 = plot.subplot_new()
subplot2.xlabel = 'X Label'
subplot2.ylabel = 'Y Label'
subplot2.plotl(x, y, color='#00FF00', linestyle='--')
subplot2.plotl(x, z, color='#0000FF', linestyle='--')
subplot2.draw()

subplot3 = plot.subplot_new()
subplot3.xlabel = 'X Label'
subplot3.ylabel = 'Y Label'
subplot3.xlimitsl = [-3, 6]
subplot3.ylimitsl = [0, 100]
subplot3.plotl(x, y + z)
subplot3.draw()

x, y = np.random.randn(2, 100)

subplot4 = plot.subplot_new()
axl = subplot4.axl
axl.xcorr(x, y, usevlines=True, maxlags=50, normed=True, lw=2)
axl.grid(True)
axl.axhline(0, color='black', lw=2)
subplot4.draw()

# TODO: this should not be necessary
plot.show()

app.show()
app.run()

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
