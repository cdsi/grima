import unittest

class PlotTestCase(unittest.TestCase):

	# FYI - unit test names must start with 'test_'

	def test_plot(self):
		pass

def testsuite():
	__testsuite = unittest.TestSuite()
	__testsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(PlotTestCase))
	return __testsuite

# Local Variables:
# indent-tabs-mode: nil
# py-indent-offset: 8
# py-smart-indentation: nil
# tab-width: 8
# End:
# vim: ai et si sw=8 ts=8
