"""
test functions of Circle()

zs. elter 2019
"""

import unittest
from feign.geometry import *

class TestCircleIntersection(unittest.TestCase):
    def test_intersection_horizontal(self):
        c=Circle(Point(1,1),5)
        s1=Segment(Point(-5.5,1),Point(7.5,1))
        self.assertEqual(c.intersection(s1)[0].x,6.0)
    def test_intersection_vertical(self):
        c=Circle(Point(1,1),5)
        s1=Segment(Point(1,-8),Point(1,10))
        self.assertTrue(-4.0 in [c.intersection(s1)[0].y, c.intersection(s1)[1].y])
    def test_intersection_any(self):
        c=Circle(Point(1,1),5)
        s1=Segment(Point(-9,-9),Point(9,9))
        self.assertTrue(len(c.intersection(s1)) == 2)
    def test_intersection_tangent(self):
        c=Circle(Point(1,1),5)
        s1=Segment(Point(-1,6),Point(9,6))
        self.assertListEqual(c.intersection(s1),[])
    def test_intersection_no(self):
        c=Circle(Point(1,1),5)
        s1=Segment(Point(7,7),Point(9,10))
        self.assertListEqual(c.intersection(s1),[])
    def test_intersection_one(self):
        c=Circle(Point(1,1),5)
        s1=Segment(Point(1,1),Point(2,9))
        self.assertTrue(len(c.intersection(s1)) == 1)


if __name__ == '__main__':
    unittest.main()

