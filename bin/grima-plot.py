#!/usr/bin/env python

import random
import sys

import numpy

from optparse import OptionParser

from grima.plot import Plot

def stats(y, x=None):
        print "  len =", len(y)
        print " mean =", numpy.mean(y)
        print "  sum =", sum(y)
        print "  std =", numpy.std(y)

        ymin = numpy.min(y)
        print " ymin =", ymin
        if x:
                print " xmin =", x[y.index(ymin)]

        ymax = numpy.max(y)
        print " ymax =", ymax
        if x:
                print " xmax =", x[y.index(ymax)]

def parse(f):
        x = []
        y = []

        fp = open(f, 'r')

        while True:
                line = fp.readline()
                if not(line):
                        break

                data = line.split(',')
                x.append(float(data[0]))
                try:
                        y.append(float(data[1]))
                except IndexError:
                        y = []

        return x, y

usage = """%prog [options] data1 data2 data3 ...

options:

--title=\"Window Title\" (default is None)"""

if __name__ == "__main__":

        op = OptionParser(usage)

        op.add_option('--title', action='store', dest='title', default=None,
                      help='"Window Title" (default is None)')

        (options, args) = op.parse_args()

        p = Plot()
        p.enabled = True
        p.type = 'window'
        p.show()

        if options.title:
                # p.title = title
                print title

        color = 0xFF0000

        for f in (sys.argv[1:]):
                print 'data: ', f
                x, y = parse(f)

                if len(y):
                        p.plotl(x, y, color=color)
                        stats(y, x=x)
                else:
                        p.ploth(x, color=color)
                        stats(x)

                color = int(random.getrandbits(24))

        p.draw()
        p.run()

# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
