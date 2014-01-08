from islplot.plotter import *
from islpy import *

import unittest
from test import support

class TestPlotter(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_do_not_fail_on_empty_bset(self):
        plot_bset_shape(BasicSet("{[i,j]: 1 = 0}"))

if __name__ == '__main__':
    unittest.main()
