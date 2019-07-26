#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test functions of Point()

zs. elter 2019
"""

import unittest
#from feign.geometry import *

class TestInBetween(unittest.TestCase):
    def test_inbetween_in_45deg(self):
        self.assertTrue(Point(2,2).inBetween(Point(1,1),Point(4,4)))
    def test_inbetween_in_someline(self):
        self.assertTrue(Point(1.85,1.89).inBetween(Point(0,3),Point(5,0)))
    def test_inbetween_endpoint(self):
        self.assertTrue(Point(0,3).inBetween(Point(0,3),Point(5,0)))
    def test_inbetween_vertical(self):
        self.assertTrue(Point(1,5.5).inBetween(Point(1,3),Point(1,7)))
    def test_inbetween_horizontal(self):
        self.assertTrue(Point(7,5.5).inBetween(Point(5,5.5),Point(10,5.5)))
    def test_inbetween_out_45deg(self):
        self.assertFalse(Point(-1,-1).inBetween(Point(1,1),Point(4,4)))
    def test_inbetween_out_someline(self):
        self.assertFalse(Point(-2.42,4.45).inBetween(Point(0,3),Point(5,0)))
    def test_inbetween_not_on_line(self):
        self.assertFalse(Point(-2.3,4.3).inBetween(Point(0,3),Point(5,0)))
        
class TestIsEqual(unittest.TestCase):
    def test_isequal_1(self):
        P=Point(3.445,5.232)
        Q=Point(3.445,5.232)
        self.assertTrue(P.isEqual(Q))
    def test_isequal_2(self):
        P=Point(3.445,5.232)
        Q=Point(3.445,6.232)
        self.assertFalse(P.isEqual(Q))
        
class TestRotate(unittest.TestCase):
    def test_rotate1(self):
        P=Point(3,4)
        Q=P.rotate(90)
        self.assertEqual(Q.x,-4.0)
    def test_rotate2(self):
        P=Point(3,4)
        Q=P.rotate(-90)
        self.assertEqual(Q.x,4.0)

class TestTranslate(unittest.TestCase):
    def test_translate(self):
        P=Point(3,4)
        Q=P.translate(6,2)
        self.assertEqual(Q.x,9)
        
class TestDistance(unittest.TestCase):
    def test_distance_horizontal(self):
        self.assertEqual(Point.distance(Point(3,4),Point(3,7)),3)
    def test_distance_vertical(self):
        self.assertEqual(Point.distance(Point(3,4),Point(2,4)),1)
    def test_distance_1(self):
        self.assertEqual(Point.distance(Point(3,4),Point(5,6)),np.sqrt(8))
    def test_distance_2(self):
        self.assertEqual(Point(3,4).distance(Point(5,6)),np.sqrt(8))
    def test_distance_to_self(self):
        self.assertEqual(Point(3,4).distance(Point(3,4)),0)
    


if __name__ == '__main__':
    unittest.main()