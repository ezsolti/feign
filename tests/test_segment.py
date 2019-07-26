#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test functions of Segment()

zs. elter 2019
"""

import unittest
from feign.geometry import *

class TestSegmentIntersection(unittest.TestCase):
    def test_intersection_parallel(self):
        s1=Segment(Point(3,4),Point(5,7))
        s2=Segment(Point(1,4),Point(3,7))
        self.assertListEqual(s1.intersection(s2),[])
    def test_intersection_horiz_vertic_yes(self):
        s1=Segment(Point(3,4),Point(7,4))
        s2=Segment(Point(5,6),Point(5,2))
        self.assertEqual(s1.intersection(s2)[0].x,5.0)
    def test_intersection_horiz_vertic_no(self):
        s1=Segment(Point(3,4),Point(7,4))
        s2=Segment(Point(2,6),Point(2,2))
        self.assertListEqual(s1.intersection(s2),[])
    def test_intersection_vertic_and_other(self):
        s1=Segment(Point(4,3),Point(6,5))
        s2=Segment(Point(5,6),Point(5,2))
        self.assertEqual(s1.intersection(s2)[0].y,4.0)
    def test_intersection_endpoint(self):
        s1=Segment(Point(3,4),Point(7,4))
        s2=Segment(Point(7,4),Point(1,9))
        self.assertEqual(s1.intersection(s2)[0].x,7.0)
    def test_intersection_yes(self):
        s1=Segment(Point(2,2),Point(-2,-2))
        s2=Segment(Point(-2,2),Point(2,-2))
        self.assertEqual(s1.intersection(s2)[0].x,0.0)
    def test_intersection_no(self):
        s1=Segment(Point(2,2),Point(-2,-2))
        s2=Segment(Point(-3,-4),Point(-6,-7))
        self.assertListEqual(s1.intersection(s2),[])



if __name__ == '__main__':
    unittest.main()

