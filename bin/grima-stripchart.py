from __future__ import division
from __future__ import with_statement

from optparse import OptionParser

import numpy as np

import elrond.widgets
import grima.widgets

from elrond.ui import Window
from grima.plot2 import Plot

x = np.arange(0, 3, .02)
y = np.sin(2 * np.pi * x)
z = np.cos(2 * np.pi * x)

def producer1():
        __y = []

        while True:
                if not __y:
                        __y = list(y)

                yield [(__y.pop(0))]

def producer2():
        __z = []

        while True:
                if not __z:
                        __z = list(z)

                yield [(__z.pop(0))]

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
stripchart1.ylimitsl = [-1, 1]

stripchart2 = plot.stripchart_new()
stripchart2.ylimitsl = [-1, 1]

stripchart1.play(producer1, interval=.5000, duration=10)
stripchart2.play(producer2, interval=.0001, duration=50)

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
