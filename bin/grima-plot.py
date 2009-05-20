#!/usr/bin/env python

import json

from optparse import OptionParser

from grima.plot import Plot

if __name__ == "__main__":

        op = OptionParser('%prog [options] data1 data2 data3 ...')

        op.add_option('--title', action='store', dest='title', default=None,
                      help='title to be used in plot window')
        op.add_option('--type', action='store', dest='type', default='window',
                      help='[console | window | image:filename] default is window')

        (options, args) = op.parse_args()

        p = Plot()

        p.type = options.type
        p.title = options.title

        p.enabled = True
        p.overlay = True

        for filename in args:
                with open(filename, 'r') as f:
                        for data in json.load(f):
                                p.plotl(data['x'], data['y'], xlabel=data['xlabel'], ylabel=data['ylabel'],
                                        style=data['style'], color=data['color'])

        p.show()
        p.draw()
        p.run()

# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
