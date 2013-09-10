from polynomials import *
import unittest

# to use unittest, just create a class and subclass unittest's TestCase class
class TestPoly(unittest.TestCase):

    def setUp(self):
        self.p1 = poly((10, 20, 30))
        self.p3 = poly((0, 0, 0, 1))

    def test_out(self):
        """poly should be a function that correctly calculates values"""
        self.assertEqual(self.p1(0), 10)
        for x in (1, 2, 3, 4, 5, 1234.5):
            self.assertEqual(self.p1(x), 30 * x**2 + 20 * x + 10)

# to run the tests:
if __name__ == '__main__':
    unittest.main(verbosity=2)