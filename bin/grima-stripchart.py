from __future__ import division
from __future__ import with_statement

from optparse import OptionParser

import numpy as np

from elrond.ui import Window
from grima.plot2 import Plot

def callback():
        pass

op = OptionParser('%prog [options] data1 data2 data3 ...')

op.add_option('--title', action='store', dest='title', default=None,
              help='title to be used in plot window')

(options, args) = op.parse_args()

plot = Plot()
plot.overlay = True

window = Window(widget=plot)
window.title = options.title

x = np.arange(0,3,.02)
y = np.exp(x)
z = y[::-1]

stripchart1 = plot.stripchart_new(callback)
plot.stripchart_delete(stripchart1)

stripchart2 = plot.stripchart_new(callback)
stripchart2.plotl(x, y, color=0x00FF00, style='--')
stripchart2.plotl(x, z, color=0x0000FF, style='--')

stripchart3 = plot.stripchart_new(callback)
stripchart3.plotl(x, y + z, xlabel='X Label', ylabel='Y Label')
stripchart3.set_limitsl([-3, 6, 0, 100])

window.show()
window.run()

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
