from __future__ import division
from __future__ import with_statement

from optparse import OptionParser

import numpy as np

from elrond.ui import Window
from grima.plot2 import Plot

x = np.arange(0, 3, .02)
y = np.sin(2 * np.pi * x)
z = np.cos(2 * np.pi * x)

def callback1():
        i = 0
        while True:
                yield [(x[i], y[i])]
                i += 1

def callback2():
        i = 0
        while True:
                yield [(x[i], z[i])]
                i += 1

op = OptionParser('%prog [options]')

op.add_option('--socket', action='store', dest='socket', default=None,
              help='The named pipe created by mkfifo')

op.add_option('--title', action='store', dest='title', default=None,
              help='The subplot window title.')
op.add_option('--deletable', action='store', dest='deletable', default=True,
              help='When disabled the subplot window is not closable.')

(options, args) = op.parse_args()

# TODO: if options.socket == None:
# TODO:         op.error('--socket=... is required')

socket = options.socket

plot = Plot()
plot.overlay = False

window = Window(widget=plot)
window.title = options.title
window.deletable = options.deletable

stripchart1 = plot.stripchart_new()
stripchart1.limitsl = [0, 10, -2, 2]

stripchart2 = plot.stripchart_new()
stripchart2.limitsl = [0, 20, -2, 2]

stripchart1.play(callback1, interval=2/10)
stripchart2.play(callback2, interval=1/10)

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
