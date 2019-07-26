#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test Point
"""

import unittest
from feign.geometry import *

class TestInBetween(unittest.TestCase):
    def test_inbetween_sameY(self):
        p1=Point(3,4)
        result=p1.inBetween(Point(2,4),Point(4,4))
        self.assertTrue(result)

    def test_inbetween_sameX(self):
        p1=Point(5,3)
        result=p1.inBetween(Point(5,2),Point(5,4))
        self.assertTrue(result)

    def test_inbetween_samePoint(self):
        p1=Point(5,3)
        result=p1.inBetween(Point(5,3),Point(5,4))
        self.assertTrue(result)
        
class TestIsEqual(unittest.TestCase):
    def test_isequal_1(self):
        P=Point(3.445,5.232)
        Q=Point(3.445,5.232)
        self.assertTrue(P.isEqual(Q))
    def test_isequal_2(self):
        P=Point(3.445,5.232)
        Q=Point(3.445,6.232)
        self.assertFalse(P.isEqual(Q))


if __name__ == '__main__':
    unittest.main()