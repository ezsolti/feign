# -*- coding: utf-8 -*-
"""
FEIGNgeom 
"""
import math
import numpy as np
eps=1e-7

class Point(object):
    """
    A class used to represent a Point.
    
    Parameters
    ----------   
    X : float
        x coordinate of Point in cm
    Y : float
        y coordinate of Point in cm
      
    Attributes
    ----------
    x : float
        x coordinate of Point in cm
    y : float
        y coordinate of Point in cm
    """

    def __init__(self, X, Y):
        self.x = X
        self.y = Y

    def __repr__(self):
        return "Point(%.3f, %.3f)" % (self.x, self.y)

    def distance(self, other):
        """The function calculates the distance of two Point objects.
        
        Parameters
        ----------
        other : Point()
            the Point to which the distance is calculated
          
        Returns
        -------
        float
            distance of two points
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)
        
    def inBetween(self,p1,p2):
        """The function to assess whether a Point() is on the same line and
        in between two other Point() objects.
        
        Parameters
        ----------
        p1,p2 : Point()
            Points for which the test point is checked whether is placed in between.
          
        Returns
        -------
        bool
            True if the point is between p1 and p2, False otherwise
        
        Examples
        --------
        >>> Point(2,2).inBetween(Point(1,1),Point(4,4))
        True
        >>> Point(-2.3,4.3).inBetween(Point(0,3),Point(5,0))
        False
        """
        dxc = self.x - p1.x
        dyc = self.y - p1.y
        dxl = p2.x - p1.x
        dyl = p2.y - p1.y
        
        if abs(dxc*dyl-dyc*dxl)<=eps:
            if abs(dxl)>=abs(dyl): 
                if dxl>0:
                    return p1.x-self.x <= eps and self.x-p2.x <= eps
                else:
                    return p2.x-self.x <= eps and self.x-p1.x <= eps
            else:
                if dyl>0:
                    return p1.y-self.y <= eps and self.y-p2.y <= eps
                else:
                    return p2.y-self.y <= eps and self.y-p1.y <= eps
        else:
            return False
        
    def isEqual(self, other):
        """The function to assess whether two Point() objects are the same.
        
        Parameters
        ----------
        other : Point()
            point with which the equality is checked.
          
        Returns
        -------
        bool
            True if the points are equal, False otherwise
        
        Examples
        --------
        >>> p=Point(3,3)
        >>> q=Point(3,3)
        >>> p.isEqual(q)
        True
        >>> a=Point(3,4)
        >>> p.isEqual(a)
        False
        """
        if abs(self.x-other.x)<eps and abs(self.y-other.y)<eps:
            return True
        else:
            return False
        
        
    def rotate(self,alpha):
        """The function to rotate a Point around the origin with alpha (deg)
        
        Parameters
        ----------
        alpha : float
            Rotation angle (in degrees)
           
        Returns
        -------
        Point()
            Point with rotated coordinates
        
        Examples
        --------
        >>> Point(10,0).rotate(90)
        Point(0.000, 10.000)
        >>> Point(10,0).rotate(45)
        Point(7.071, 7.071)
        """
        
        alpha=alpha*(np.pi/180.0)
        return Point(self.x*np.cos(alpha)-self.y*np.sin(alpha),self.y*np.cos(alpha)+self.x*np.sin(alpha))
        
    def translate(self,xt,yt):
        """The function to translate a Point
        
        Parameters
        ----------
        xt : float
            translation along x direction
        yt : float
            translation along y direction
           
        Returns
        -------
        Point() 
            Point with translated coordinates
        
        Examples
        --------
        >>> Point(10,0).translate(5,3)
        Point(15.000, 3.000)
        """
        return Point(self.x+xt,self.y+yt)


class Segment(object):
    """
    A class used to represent a Segment.
    
    Parameters
    ----------   
    P : Point()
        first end point of Segment
    Q : Point()
        second end point of Segment
      
    Attributes
    ----------
    p : Point()
        first end point of Segment
    q : Point()
        second end point of Segment
    slope: float
        slope of the line (np.Inf if vertical)
    intercept: float
        intercept on the y axis (intercept on the x axis if vertical)
    points: list of Point()
        list of p and q

    """
    def __init__(self,P,Q):
        self.p=P
        self.q=Q
        self._points=[P,Q]
        if abs(Q.x-P.x)<eps:
            self._slope=np.Inf
            self._intercept=Q.x
            #in this case the x coordinate is returned as the intercept!
            #the intersection functions will make use of this            
        else:
            self._slope=(Q.y-P.y)/(Q.x-P.x)
            self._intercept=P.y-self._slope*P.x
            
    def __repr__(self):
        return "Segment(Point(%.3f, %.3f),Point(%.3f, %.3f))" % (self.p.x, self.p.y,self.q.x, self.q.y)
    
    @property
    def slope(self):
        return self._slope

    @property
    def intercept(self):
        return self._intercept

    @property
    def points(self):
        return self._points
    
    def intersection(self,other):
        """The function to find the intersection of two Segment objects.
        
        Parameters
        ----------
        other : Segment()
            The Segment() for which the intersection is calculated
           
        Returns
        -------
        list of Point()
            list of the intersections
        
        Notes
        -----
        The list has one element if the Segments intersect (even if only through
        their end points).
        
        An empty list is returned if the Segments do not have an intersection.
        
        Examples
        --------
        >>> s1=Segment(Point(2,2),Point(-2,-2))
        >>> s2=Segment(Point(-2,2),Point(2,-2))
        >>> s1.intersection(s2)
         [Point(0.000, 0.000)]
        >>> s3=Segment(Point(-3,-4),Point(-6,-7))
        >>> s1.intersection(s3)
         []
        """
         
        if abs(self.slope-other.slope)<eps: #parallel
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
        """The function to rotate a Segment around the origin with alpha (deg)
        
        Parameters
        ----------
        alpha : float
            Rotation angle (in degrees)
           
        Returns
        -------
        Segment()
            Segment with rotated end points
        """
        return Segment(self.p.rotate(alpha),self.q.rotate(alpha))

class Circle(object):
    """
    A class used to represent a Circle.

    Parameters
    ----------   
    C : Point()
        center of Circle
    R : float
        radius of Circle
    
    Attributes
    ----------   
    c : Point()
        center of Circle
    r : float
        radius of Circle
    """

    def __init__(self, C, R):
        self.c = C
        self.r = R

    def __repr__(self):
        return "Circle(C=(%.3f, %.3f),R=%.3f)" % (self.c.x, self.c.y,self.r)

    def intersection(self,seg):
        """The function to find the intersection of a Circle with a Segment.
        
        Parameters
        ----------
        seg : Segment()
            The Segment for which the intersection is calculated
           
        Returns
        -------
        list of Point()
            list of the intersection

        Notes
        -----
        The returned list has one element if one of the endpoints of the Segment is 
        enclosed by the circle.
        
        The list has two elements if both endpoints of the Segment lies outside
        the Circle and the Segment passes through the circle.
        
        An empty list is returned if the Segment does not pass through the Circle, 
        or in case the Segment is a tangent.
        
        Examples
        --------
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
            if D <= eps:
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
        """The function to assess whether a point is enclosed by a Circle.
        
        Parameters
        ---------- 
        P : Point()
            point to decide whether is enclosed by the Circle
        
        Returns
        -------
        bool
            True if P is enclosed by the Circle, False otherwise
        
        Examples
        --------
        >>> c=Circle(Point(1,1),5)
        >>> P=Point(3,4)
        >>> c.encloses_point(P)
        True
        >>> Q=Point(4,3)
        >>> c=Circle(Point(1,1),5)
        False
        """
        if Point.distance(self.c,P)<self.r+eps:
            return True
        else:
            return False

        
class Rectangle(object):
    """
    A class used to represent a Rectangle. 
    
    Rectangles are actually general convex quadritlaterals.
    To create a Rectangle, one should give the four corners in a clockwise or
    counter-clockwise order
    
    Parameters
    ----------
    P1 : Point()
        first corner
    P2 : Point()
        second corner
    P3 : Point()
        third corner
    P4 : Point()
        fourth corner
    
    Attributes
    ----------   
    p1 : Point()
        first corner
    p2 : Point()
        second corner
    p3 : Point()
        third corner
    p4 : Point()
        fourth corner
    p1p2 : Segment()
        first side
    p2p3 : Segment()
        second side
    p3p4 : Segment()
        third side
    p4p1 : Segment()
        fourth side
    corners : list of Point()
        list of the corner points
    sides : list of Segment()
        list of the sides
        
    Raises
    ------
    ValueError
        if Corners are not defined in clockwise or counter-clockwise order.
    """
    def __init__(self,P1,P2,P3,P4):
        self.p1=P1
        self.p2=P2
        self.p3=P3
        self.p4=P4
        self._corners=[P1,P2,P3,P4]
        if Segment(P1,P3).intersection(Segment(P2,P4)) == []:
            raise ValueError('Corners defined in wrong order')
        else:
            self._p1p2=Segment(P1,P2)
            self._p2p3=Segment(P2,P3)
            self._p3p4=Segment(P3,P4)
            self._p4p1=Segment(P4,P1)
            self._sides=[self._p1p2,self._p2p3,self._p3p4,self._p4p1]
        
    def __repr__(self):
        return "Rectangle(Point(%.3f, %.3f),Point(%.3f, %.3f),Point(%.3f, %.3f),Point(%.3f, %.3f))" % (self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.p3.x, self.p3.y, self.p4.x, self.p4.y)

    @property
    def p1p2(self):
        return self._p1p2    

    @property
    def p2p3(self):
        return self._p2p3
    
    @property
    def p3p4(self):
        return self._p3p4
    
    @property
    def p4p1(self):
        return self._p4p1
    
    @property
    def corners(self):
        return self._corners
    
    @property
    def sides(self):
        return self._sides
    
    def encloses_point(self,P):
        """ The function to assess whether a point is enclosed by a Rectangle().
        
        Parameters
        ----------
        P : Point()
            point to decide whether is enclosed by Rectangle
        
        Returns
        -------
        bool
            True if the point is enclosed by the Rectangle, False otherwise. 
        
        Examples
        --------
        >>> rect=Rectangle(Point(3,7),Point(5,3),Point(13,5),Point(12,6))
        >>> P=Point(6,5)
        >>> rect.encloses_point(P)
        True
        >>> Q=Point(4,3)
        >>> rect.encloses_point(Q)
        False
        """
        #In case of a rectangle ABCD and point P, the function computes the area
        #of triangles PAB, PBC, PCD and PDA with Heron's formula. Then it computes
        #the area of the rectangle by evaluating the areas of the triangles ABC
        #and ACD. If A_PAB+A_PBC+A_PCD+A_PDA>A_ABC+A_ACD then the function returns
        #False. Otherwise True is returned.
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
        
        if abs(Atris-Arect)<eps:
            return True
        else:
            return False

    def rotate(self,alpha):
        """The function to rotate a Rectangle around the origin with alpha (deg)
        
        Parameters
        ----------
        alpha : float
            Rotation angle (in degrees)
           
        Returns
        -------
        Rectangle()
            Rectangle with rotated end points
        """
        return Rectangle(self.p1.rotate(alpha),self.p2.rotate(alpha),self.p3.rotate(alpha),self.p4.rotate(alpha))


    def intersection(self,seg):
        """The function to find the intersection of a Rectangle with a Segment.
        
        Parameters
        ----------
        seg : Segment()
            The Segment for which the intersection is calculated
           
        Returns
        -------
        list of Point()
            list of the intersections
        
        Notes
        -----

        The list has one element if one of the endpoints of the Segment is 
        enclosed by the rectangle.
        
        The list has two elements if both endpoints of the Segment lies outside
        the Rectangle, and the Segment passes through the Rectangle.
        
        An empty list is returned if the Segment does not pass through the Rectangle, 
        or in case the Segment passes through only one of the corners.
        
        Examples
        --------
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
                print(self)
                print(seg)
                print(self.p1)
                print(self.p2)
                print(self.p3)
                print(self.p4)
                print(seg.p)
                print(seg.q)
                import code
                code.interact(local=dict(globals(), **locals()))
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
                