#!/usr/bin/env python

import sys

import numpy
import pylab

def stats(x):
	print "  num =", len(x)
	print "  min =", numpy.min(x)
	print "  max =", numpy.max(x)
	print " mean =", numpy.mean(x)
	print "  sum =", sum(x)
	print "  std =", numpy.std(x)

def plot(f):
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

	if len(y):
		pylab.plot(x, y)
		print f + ":"
		stats(y)
	else:
		pylab.plot(x)
		print f + ":"
		stats(x)

	pylab.title(f)
	pylab.show()

for f in (sys.argv[1:]):
	plot(f)
