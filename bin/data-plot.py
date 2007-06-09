#!/usr/bin/env python

import sys

import numpy
import pylab

from gandalf.backends import HUL

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

	HUL.stats(y, label=filename)

	pylab.plot(y)
	pylab.title(filename)
	pylab.show()

for filename in sys.argv[1:]:
    plot(filename)
