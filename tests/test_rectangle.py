"""
test functions of Rectangle()

zs. elter 2019
"""

import unittest
from feign.geometry import *

class TestRectangleDefinition(unittest.TestCase):
    def test_rectangle_wrong_corner_order(self):
        with self.assertRaises(ValueError):
            rect=Rectangle(Point(3,7),Point(13,5),Point(5,3),Point(12,6))
    def test_rectangle_concave_shape(self):
        with self.assertRaises(ValueError):
            rect=Rectangle(Point(5,3),Point(13,5),Point(10,7),Point(10,10))


class TestEnclosesPoint(unittest.TestCase):
    def test_encloses_point_yes(self):
        rect=Rectangle(Point(3,7),Point(5,3),Point(13,5),Point(12,6))
        self.assertTrue(rect.encloses_point(Point(6,5)))
    def test_encloses_point_no(self):
        rect=Rectangle(Point(3,7),Point(5,3),Point(13,5),Point(12,6))
        self.assertFalse(rect.encloses_point(Point(4,3)))

class TestRectIntersection(unittest.TestCase):
    def test_rect_intersect_segment_out(self):
        rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        s=Segment(Point(11,11),Point(13,17))
        self.assertListEqual(rect.intersection(s),[])
    def test_rect_intersect_segment_out_through_corner(self):
        rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        s=Segment(Point(0,20),Point(20,0))
        self.assertListEqual(rect.intersection(s),[])
    def test_rect_intersect_segment_one_endpoint_in(self):
        rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        s=Segment(Point(0,0),Point(0,20))
        with self.subTest():
            self.assertEqual(len(rect.intersection(s)),1)
        with self.subTest():
            self.assertTrue(rect.intersection(s)[0].isEqual(Point(0,10)))
    def test_rect_intersect_segment_one_endpoint_in_through_corner(self):
        rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        s=Segment(Point(0,0),Point(20,20))
        with self.subTest():
            self.assertEqual(len(rect.intersection(s)),1)
        with self.subTest():
            self.assertTrue(rect.intersection(s)[0].isEqual(Point(10,10)))

    def test_rect_intersect_segment_two_intersection_general(self):
        rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        s=Segment(Point(0,15),Point(15,0))
        inters=rect.intersection(s)
        with self.subTest():
            self.assertEqual(len(inters),2)
        with self.subTest():
            self.assertTrue(inters[0].isEqual(Point(10,5)) or inters[1].isEqual(Point(10,5)))
        with self.subTest():
            self.assertTrue(inters[0].isEqual(Point(5,10)) or inters[1].isEqual(Point(5,10)))

    def test_rect_intersect_segment_two_intersection_one_through_corner(self):
        rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        s=Segment(Point(-30,30),Point(15,0))
        inters=rect.intersection(s)
        with self.subTest():
            self.assertEqual(len(inters),2)
        with self.subTest():
            self.assertTrue(inters[0].isEqual(Point(10,10/3)) or inters[1].isEqual(Point(10,10/3)))
        with self.subTest():
            self.assertTrue(inters[0].isEqual(Point(0,10)) or inters[1].isEqual(Point(0,10)))
    
    def test_rect_intersect_segment_two_intersection_two_through_corner(self):
        rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        s=Segment(Point(-30,-30),Point(30,30))
        inters=rect.intersection(s)
        with self.subTest():
            self.assertEqual(len(inters),2)
        with self.subTest():
            self.assertTrue(inters[0].isEqual(Point(10,10)) or inters[1].isEqual(Point(10,10)))
        with self.subTest():
            self.assertTrue(inters[0].isEqual(Point(-10,-10)) or inters[1].isEqual(Point(-10,-10)))
            

if __name__ == '__main__':
    unittest.main()

