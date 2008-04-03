#!/usr/bin/env python

import sys

import numpy

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

for f in (sys.argv[1:]):
	x = []
	y = []

	fp = open(f, 'r')

	while True:
		line = fp.readline()
		if not(line):
			break
		
		_ = line.split(',')
		x.append(float(_[0]))
		try:
			y.append(float(_[1]))
		except IndexError:
			y = []

	p = Plot()
	p.enabled = True
	p.type = 'window'
	p.show()

	print 'data: ', f

	if len(y):
		p.plotl(x, y)
		stats(y, x=x)
	else:
		p.ploth(x)
		stats(x)

	p.draw()
	p.run()

# Local Variables:
# indent-tabs-mode: nil
# py-indent-offset: 8
# py-smart-indentation: nil
# tab-width: 8
# End:
# vim: ai et si sw=8 ts=8
