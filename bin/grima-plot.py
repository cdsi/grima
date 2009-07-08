from __future__ import division
from __future__ import with_statement

from optparse import OptionParser

from grima.plot import Plot

if __name__ == "__main__":

        op = OptionParser('%prog [options] data1 data2 data3 ...')

        op.add_option('--title', action='store', dest='title', default=None,
                      help='title to be used in plot window')
        op.add_option('--type', action='store', dest='type', default='window',
                      help='[console | window | image:filename] default is window')

        (options, args) = op.parse_args()

        plot = Plot()

        plot.type = options.type
        plot.title = options.title

        plot.enabled = True
        plot.overlay = True

        plot.show()
        plot.draw()

        for i, filename in enumerate(args):
                plot.open(filename, i=i)

        plot.run()

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
