#!/usr/bin/env python

import random
import re
import sys

import numpy

from optparse import OptionParser

from grima.plot import Plot

def stats(x, y):
        print "  len =", len(y)
        print " mean =", numpy.mean(y)
        print "  sum =", sum(y)
        print "  std =", numpy.std(y)

        ymin = numpy.min(y)
        print " ymin =", ymin
        print " xmin =", x[y.index(ymin)]

        ymax = numpy.max(y)
        print " ymax =", ymax
        print " xmax =", x[y.index(ymax)]

def parse(f):
        x = []
        y = []

        fd = open(f, 'r')
        lines = [l.strip() for l in fd.readlines()]
        fd.close()

        for i, line in enumerate(lines):
                data = filter(lambda x: x != '', re.split('[, ]', line.strip()))

                try:
                        y.append(float(data[1]))
                        x.append(float(data[0]))
                except IndexError:
                        y.append(float(data[0]))
                        x.append(i)

        return x, y

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

        color = 0xFF0000

        for f in args:
                print 'data:', f
                x, y = parse(f)

                p.plotl(x, y, color=color)
                stats(x, y)

                color = int(random.getrandbits(24))

        p.show()
        p.draw()
        p.run()

# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
