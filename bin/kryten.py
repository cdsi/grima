#!/usr/bin/env python

import sys

import numpy
import pylab

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

def plot(f):
	x = []
	y = []

	fp = open(f, 'r')
	while True:
		line = fp.readline()
		if not(line):
			break
		
		_ = line.split(', ')
		x.append(float(_[0]))
		try:
			y.append(float(_[1]))
		except IndexError:
			y = []

	if len(y):
		pylab.plot(x, y)
		print f + ":"
		stats(y, x=x)
	else:
		pylab.plot(x)
		print f + ":"
		stats(x)

	pylab.title(f)
	pylab.show()

for f in (sys.argv[1:]):
	plot(f)
