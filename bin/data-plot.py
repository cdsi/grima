#!/usr/bin/env python

import string, sys
import numpy
import pylab

def plot(filename):
	y = []

	file = open(filename, 'r')
	while True:
		line = file.readline()
		if not(line):
			break
		y.append(string.atof(line))

	print filename + ":"
	print "  num =", len(y)
	print "  min =", numpy.min(y)
	print "  max =", numpy.max(y)
	print " mean =", numpy.mean(y)
	print "  sum =", sum(y)
	print "  std =", numpy.std(y)

	pylab.plot(y)
	pylab.show()

plot(sys.argv[1])
