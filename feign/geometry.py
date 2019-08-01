# -*- coding: utf-8 -*-
"""
FEIGNgeom 
"""
import math
import numpy as np

class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''

    def __init__(self, X, Y):
        '''Defines a Point with x and y coordinates'''
        self.x = X
        self.y = Y

    def __repr__(self):
        return "Point(%.3f, %.3f)" % (self.x, self.y)

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)
        
    def inBetween(self,p1,p2):
        """Function to assess whether a Point() is on the same line and
        in between two other Point() objects. True is returned even if the point
        is the same as one of the other two points.
        Input: three Point() object
        Output: boolean
        >>> Point(2,2).inBetween(Point(1,1),Point(4,4))
        True
        >>> Point(-2.3,4.3).inBetween(Point(0,3),Point(5,0))
        False
        """
        dxc = self.x - p1.x
        dyc = self.y - p1.y
        dxl = p2.x - p1.x
        dyl = p2.y - p1.y
        
        if abs(dxc*dyl-dyc*dxl)<=0.00001:
            if abs(dxl)>=abs(dyl): 
                if dxl>0:
#                    return p1.x <= self.x and self.x <= p2.x
                    return p1.x-self.x <= 0.00001 and self.x-p2.x <= 0.00001
                else:
                    return p2.x-self.x <= 0.00001 and self.x-p1.x <= 0.00001
            else:
                if dyl>0:
                    return p1.y-self.y <= 0.00001 and self.y-p2.y <= 0.00001
                else:
                    return p2.y-self.y <= 0.00001 and self.y-p1.y <= 0.00001
        else:
            return False
        
    def isEqual(self, other):
        """
        Function to assess whether two Point() objects are the same.
        Inputs: two Point() objects
        Output: boolean
        >>> p=Point(3,3)
        >>> q=Point(3,3)
        >>> p.isEqual(q)
        True
        >>> a=Point(3,4)
        >>> p.isEqual(a)
        False
        """
        if abs(self.x-other.x)<0.00001 and abs(self.y-other.y)< 0.00001:
            return True
        else:
            return False
        
        
    def rotate(self,alpha):
        """Rotation around the origin with alpha (deg)"""
        alpha=alpha*(np.pi/180.0)
        return Point(self.x*np.cos(alpha)-self.y*np.sin(alpha),self.y*np.cos(alpha)+self.x*np.sin(alpha))
        
    def translate(self,xt,yt):
        return Point(self.x+xt,self.y+yt)

class Segment(object):
    def __init__(self,P,Q):
        """Segment() object is defined with the two end points (Point() objects).
        Attributes:
            p: first end point
            q: second end point
            slope: slope of the line (np.Inf if vertical)
            intercept: intercept of the y axis (intercept of x axis if vertical)
        """
        self.p=P
        self.q=Q
        if abs(Q.x-P.x)<0.00001:
            self.slope=np.Inf
            self.intercept=Q.x
            #in this case the x coordinate is returned as the intercept!
            #the intersection functions will make use of this            
        else:
            self.slope=(Q.y-P.y)/(Q.x-P.x)
            self.intercept=P.y-self.slope*P.x
            
    def __repr__(self):
        return "Segment(Point(%.3f, %.3f),Point(%.3f, %.3f))" % (self.p.x, self.p.y,self.q.x, self.q.y)
        
    def intersection(self,other):
        """The function finds the intersection of two Segment objects.
        Input: two Segment() objects
        Output: a list of the intersection
        The list has one element if the Segments intersect (even if only through
        their end points).
        An empty list is returned if the Segments do not have an intersection.
        >>> s1=Segment(Point(2,2),Point(-2,-2))
        >>> s2=Segment(Point(-2,2),Point(2,-2))
        >>> s1.intersection(s2)
         [Point(0.000, 0.000)]
        >>> s3=Segment(Point(-3,-4),Point(-6,-7))
        >>> s1.intersection(s3)
         []
        """
         
        if abs(self.slope-other.slope)<0.00001: #parallel
            return []
        elif self.slope==np.Inf and other.slope!=np.Inf:
            inter=Point(self.intercept,other.slope*self.intercept+other.intercept)
        elif self.slope!=np.Inf and other.slope==np.Inf:
            inter=Point(other.intercept,self.slope*other.intercept+self.intercept)
        else:
            inter=Point((other.intercept-self.intercept)/(self.slope-other.slope),(self.slope*other.intercept-other.slope*self.intercept)/(self.slope-other.slope))

        if inter.inBetween(self.p,self.q) and inter.inBetween(other.p,other.q):
            return [inter]
        else:
            return []
        
    def rotate(self,alpha):
        """Rotation around the origin with alpha (deg)"""
        return Segment(self.p.rotate(alpha),self.q.rotate(alpha))

class Circle(object):
    def __init__(self, C, R):
        '''Defines a Circle() object with its center (Point()) and radius'''
        self.c = C
        self.r = R

    def __repr__(self):
        return "Circle(C=(%.3f, %.3f),R=%.3f)" % (self.c.x, self.c.y,self.r)

    def intersection(self,seg):
        """The function finds the intersections of a Segment with a Circle.
        Input: Circle() and Segment() object
        Output: intersections in a list.
        The list has one element if one of the endpoints of the Segment is 
        enclosed by the circle.
        The list has two elements if both endpoints of the Segment lies outside
        the Circle and the Segment passes through the circle.
        An empty list is returned if the Segment does not pass through the Circle, 
        or in case the Segment is a tangent.
        >>> c=Circle(Point(1,1),5)
        >>> s1=Segment(Point(-4,-8),Point(-4,10))
        >>> c.intersection(s1)
        []
        >>> s2=Segment(Point(3,1),Point(9,1))
        >>> c.intersection(s2)
        [Point(6.000, 1.000)]
        >>> s3=Segment(Point(-8,1),Point(9,1))
        [Point(6.000, 1.000), Point(-4.000, 1.000)]
        """
        if seg.slope==np.Inf:
            if seg.intercept>self.c.x-self.r and seg.intercept<self.c.x+self.r:
                y1=np.sqrt(self.r**2-(seg.intercept-self.c.x)**2)+self.c.y
                y2=-1*np.sqrt(self.r**2-(seg.intercept-self.c.x)**2)+self.c.y
                inter1=Point(seg.intercept,y1)
                inter2=Point(seg.intercept,y2)
                inters=[]
                if inter1.inBetween(seg.p,seg.q):
                    inters.append(inter1)
                if inter2.inBetween(seg.p,seg.q):
                    inters.append(inter2)
                return inters

            else:
                return []
        else:
            A=1+seg.slope**2
            B=(2*(seg.intercept-self.c.y)*seg.slope-2*self.c.x)
            C=(self.c.x**2+(seg.intercept-self.c.y)**2-self.r**2)
            D = B**2-4*A*C
            if D <= 0.00000001:
                return []
            else:
                x1 = (-B+math.sqrt(B**2-4*A*C))/(2*A)
                x2 = (-B-math.sqrt(B**2-4*A*C))/(2*A)
                y1 = seg.intercept + seg.slope*x1
                y2 = seg.intercept + seg.slope*x2
                inter1=Point(x1,y1)
                inter2=Point(x2,y2)
                inters=[]
                if inter1.inBetween(seg.p,seg.q):
                    inters.append(inter1)
                if inter2.inBetween(seg.p,seg.q):
                    inters.append(inter2)
                return inters

    def encloses_point(self,P):
        """Function to assess whether a point is enclosed by a Circle().
        >>> c=Circle(Point(1,1),5)
        >>> P=Point(3,4)
        >>> c.encloses_point(P)
        True
        >>> Q=Point(4,3)
        >>> c=Circle(Point(1,1),5)
        False
        """
        if Point.distance(self.c,P)<self.r+0.0000001:
            return True
        else:
            return False

        
class Rectangle(object):
    def __init__(self,P1,P2,P3,P4):
        """Defines a Rectangle() object. In fact Rectangle() objects can be general
        convex quadrilateral, the name was only omitted to avoid typos.
        Rectangle() objects have to be defined with the four corners (Point() objects).
        The corners have to be given either in a clockwise or counter-clockwise order.
        Othervise ValueError is returned.
        """
        self.p1=P1
        self.p2=P2
        self.p3=P3
        self.p4=P4
        if Segment(P1,P3).intersection(Segment(P2,P4)) == []:
            raise ValueError('Corners defined in wrong order')
        else:
            self.p1p2=Segment(P1,P2)
            self.p2p3=Segment(P2,P3)
            self.p3p4=Segment(P3,P4)
            self.p4p1=Segment(P4,P1)
        
    def __repr__(self):
        return "Rectangle(Point(%.3f, %.3f),Point(%.3f, %.3f),Point(%.3f, %.3f),Point(%.3f, %.3f))" % (self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.p3.x, self.p3.y, self.p4.x, self.p4.y)
                
    def encloses_point(self,P):
        """Function to assess whether a point is enclosed by a Rectangle().
        In case of a rectangle ABCD and point P, the function computes the area
        of triangles PAB, PBC, PCD and PDA with Heron's formula. Then it computes
        the area of the rectangle by evaluating the areas of the triangles ABC
        and ACD. If A_PAB+A_PBC+A_PCD+A_PDA>A_ABC+A_ACD then the function returns
        False. Otherwise True is returned.
        >>> rect=Rectangle(Point(3,7),Point(5,3),Point(13,5),Point(12,6))
        >>> P=Point(6,5)
        >>> rect.encloses_point(P)
        True
        >>> Q=Point(4,3)
        >>> rect.encloses_point(Q)
        False
        """
        a12=Point.distance(self.p1,P)
        b12=Point.distance(self.p2,P)
        c12=Point.distance(self.p1,self.p2)
        s12=0.5*(a12+b12+c12)
        A12=np.sqrt(s12*(s12-a12)*(s12-b12)*(s12-c12))
        
        a23=Point.distance(self.p2,P)
        b23=Point.distance(self.p3,P)
        c23=Point.distance(self.p2,self.p3)
        s23=0.5*(a23+b23+c23)
        A23=np.sqrt(s23*(s23-a23)*(s23-b23)*(s23-c23))
        
        a34=Point.distance(self.p3,P)
        b34=Point.distance(self.p4,P)
        c34=Point.distance(self.p3,self.p4)
        s34=0.5*(a34+b34+c34)
        A34=np.sqrt(s34*(s34-a34)*(s34-b34)*(s34-c34))
        
        a41=Point.distance(self.p4,P)
        b41=Point.distance(self.p1,P)
        c41=Point.distance(self.p4,self.p1)
        s41=0.5*(a41+b41+c41)
        A41=np.sqrt(s41*(s41-a41)*(s41-b41)*(s41-c41))
        
        Atris=A12+A23+A34+A41
        
        a123=Point.distance(self.p1,self.p2)
        b123=Point.distance(self.p2,self.p3)
        c123=Point.distance(self.p3,self.p1)
        s123=0.5*(a123+b123+c123)
        A123=np.sqrt(s123*(s123-a123)*(s123-b123)*(s123-c123))
        
        a134=Point.distance(self.p1,self.p3)
        b134=Point.distance(self.p3,self.p4)
        c134=Point.distance(self.p4,self.p1)
        s134=0.5*(a134+b134+c134)
        A134=np.sqrt(s134*(s134-a134)*(s134-b134)*(s134-c134))

        Arect=A123+A134
        
        if abs(Atris-Arect)<0.000001:
            return True
        else:
            return False

    def rotate(self,alpha):
        """Rotation of a Rectangle() around the origin with alpha (deg) by
        rotating all corners of the Rectangle().
            """
        return Rectangle(self.p1.rotate(alpha),self.p2.rotate(alpha),self.p3.rotate(alpha),self.p4.rotate(alpha))


    def intersection(self,seg):
        """Function to find the intersection of Rectangle() and Segment()
        objects.
        Input: Rectangle() and Segment() object
        Output: intersections in a list.
        The list has one element if one of the endpoints of the Segment is 
        enclosed by the rectangle.
        The list has two elements if both endpoints of the Segment lies outside
        the Rectangle, and the Segment passes through the Rectangle.
        An empty list is returned if the Segment does not pass through the Rectangle, 
        or in case the Segment passes through only one of the corners.
        >>> rect=Rectangle(Point(-10,10),Point(10,10),Point(10,-10),Point(-10,-10))
        >>> s=Segment(Point(-30,-30),Point(30,30))
        >>> rect.intersection(s)
        [Point(10.000, 10.000), Point(-10.000, -10.000)]
        """
        inters=[]
        for side in [self.p1p2,self.p2p3,self.p3p4,self.p4p1]:
            inters=inters+side.intersection(seg)  
        if len(inters)==0: #segment inside rectangle or no intersection
            return inters  
        elif len(inters)==1:
            return inters  #one endpoint of segment is inside rectangle
        elif len(inters)==2:
            if inters[0].isEqual(inters[1]): #segment hitting a corner
                if self.encloses_point(seg.p) or self.encloses_point(seg.q): #any of the endpoints are within the Rectangle()
                    return [inters[0]]
                else: #both endpoints are outside the rectangle -> not a real intersection
                    return []
            else:  #segment hits two sides not at the corner
                return inters
        elif len(inters)==3: #we know it is not concave, so if len(inters)>2, then there needs to be repetition due to corners
            if inters[0].isEqual(inters[1]):
                return [inters[0], inters[2]]
            elif inters[0].isEqual(inters[2]):
                return [inters[0],inters[1]]
            elif inters[1].isEqual(inters[2]):
                return [inters[0],inters[1]]
            else:
                raise ValueError('Seems to be three intersection')
        elif len(inters)==4:
            if   inters[0].isEqual(inters[1]) and inters[2].isEqual(inters[3]):
                return [inters[0], inters[2]]
            elif inters[0].isEqual(inters[2]) and inters[1].isEqual(inters[3]):
                return [inters[0],inters[1]]
            elif inters[0].isEqual(inters[3]) and inters[1].isEqual(inters[2]):
                return [inters[0],inters[1]]
            else:
                raise ValueError('Seems to be more than two intersection')
        else:
            raise ValueError('Seems to more than two intersection') #should never be reached, since we know it is not concave
                

#    def intersectionOld(self,seg):
#        inters=[]
#        inter12=seg.intersection(self.p1p2)
#        if len(inter12)>0:
#            inters.append(inter12[0])
#        inter23=seg.intersection(self.p2p3)
#        if len(inter23)>0:
#            notPresent=True
#            if inter23[0].isEqual(self.p2p3.p) or inter23[0].isEqual(self.p2p3.q): #if the segment passes through the vertex, it will be encountered twice.
#                for inter in inters:                                               #no need to check for the first element
#                    if inter.isEqual(inter23[0]):
#                        notPresent=False
#            if notPresent:
#                inters.append(inter23[0])
#        inter34=seg.intersection(self.p3p4)
#        if len(inter34)>0:
#            notPresent=True
#            if inter34[0].isEqual(self.p3p4.p) or inter34[0].isEqual(self.p3p4.q): #if the segment passes through the vertex, it will be encountered twice.
#                for inter in inters:
#                    if inter.isEqual(inter34[0]):
#                        notPresent=False
#            if notPresent:
#                inters.append(inter34[0])
#        inter41=seg.intersection(self.p4p1)
#        if len(inter41)>0:
#            notPresent=True
#            if inter41[0].isEqual(self.p4p1.p) or inter41[0].isEqual(self.p4p1.q): #if the segment passes through the vertex, it will be encountered twice.
#                for inter in inters:                                               
#                    if inter.isEqual(inter41[0]):
#                        notPresent=False
#            if notPresent:
#                inters.append(inter41[0])
#        
#        if len(inters)>2:
#            raise ValueError('seems to be an error, more than two intersections --> concave')
#            #this should not happen, since in Rectangle() I check for concave case
#        else:
#            return inters
#            
