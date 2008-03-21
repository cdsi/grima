import unittest

from grima.plot import test as plottest

def testsuite():
	__testsuite = unittest.TestSuite()
	__testsuite.addTest(unittest.TestLoader().loadTestsFromModule(plottest))
	return __testsuite
