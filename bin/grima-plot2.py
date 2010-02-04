from __future__ import division
from __future__ import with_statement

from optparse import OptionParser

from grima.plot2 import Plot

op = OptionParser('%prog [options] data1 data2 data3 ...')

op.add_option('--title', action='store', dest='title', default=None,
              help='title to be used in plot window')

(options, args) = op.parse_args()

plot = Plot()

plot.title = options.title

plot.show()
plot.draw()

for filename in args:
        plot.open(filename)

plot.run()

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
