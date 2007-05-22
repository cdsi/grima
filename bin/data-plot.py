#!/usr/bin/env python

import sys
import numpy
import pylab

def plot(filename):
	y = []

	file = open(filename, 'r')
	while True:
		line = file.readline()
		if not(line):
			break
		y.append(float(line))

	if len(y) == 0:
		return

	print filename + ":"
	print "  num =", len(y)
	print "  min =", numpy.min(y)
	print "  max =", numpy.max(y)
	print " mean =", numpy.mean(y)
	print "  sum =", sum(y)
	print "  std =", numpy.std(y)

	pylab.plot(y)
	pylab.show()

for data in sys.argv[1:]:
    plot(data)
