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

    def distance(oth, other):
        dx = oth.x - other.x
        dy = oth.y - other.y
        return math.sqrt(dx*dx + dy*dy)
        
    def inBetween(self,p1,p2):
        """The function evaluates whether a point is on the same line and
        in between two other points. If the point is equal to any of the other
        points, the function returns False.
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
        """lines are y=a*x+c and y=b*x+d
        if lines are parallel, empty list is returned
        function checks whether any line is perpendicular to x axis"""
         
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
        '''Define center as Point() and radius variables'''
        self.c = C
        self.r = R

    def __repr__(self):
        return "Circle(C=(%.3f, %.3f),R=%.3f" % (self.c.x, self.c.y,self.r)

    def intersection(self,seg):
        """for tangent it doesnt return anything"""
        if seg.slope==np.Inf:
            if seg.intercept>self.c.x-self.r and seg.intercept<self.c.x+self.r:
                y1=np.sqrt(self.r**2-(seg.intercept-self.c.x)**2)+self.c.y
                y2=-1*np.sqrt(self.r**2-(seg.intercept-self.c.x)**2)+self.c.y
                inter1=Point(seg.intercept,y1)
                inter2=Point(seg.intercept,y2)
                inter=[]
                if inter1.inBetween(seg.p,seg.q):
                    inter.append(inter1)
                if inter2.inBetween(seg.p,seg.q):
                    inter.append(inter2)
                return inter
#TODO tangent returns
#            elif seg.intercept=self.c.x-self.r or seg.intercept=self.c.x+self.r: #FLOAT COMPARE!!!
#                return Point(seg.intercept,self.c.y) #vertical line can only touch it at y=c.y
            else:
                return []
        else:
            A=1+seg.slope**2
            B=(2*(seg.intercept-self.c.y)*seg.slope-2*self.c.x)
            C=(self.c.x**2+(seg.intercept-self.c.y)**2-self.r**2)
            D = B**2-4*A*C
            if D < 0:
                return []
            elif D == 0:
                #x1=-B/(2*A)
                #y1=y1 = seg.intercept + seg.slope*x1
                #return [Point(x1,y1)]
                return []
            else:
                x1 = (-B+math.sqrt(B**2-4*A*C))/(2*A)
                x2 = (-B-math.sqrt(B**2-4*A*C))/(2*A)
                y1 = seg.intercept + seg.slope*x1
                y2 = seg.intercept + seg.slope*x2
                inter1=Point(x1,y1)
                inter2=Point(x2,y2)
                inter=[]
                if inter1.inBetween(seg.p,seg.q):
                    inter.append(inter1)
                if inter2.inBetween(seg.p,seg.q):
                    inter.append(inter2)
                return inter
        
class Rectangle(object):
    def __init__(self,P1,P2,P3,P4):
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
        """implement Heron's formula
        if triangle side lengths are a,b,c, then s=0.5*(a+b+c)
        area is then sqrt(s(s-a)(s-b)(s-c))
        """
        a12=distance(self.p1,P)
        b12=distance(self.p2,P)
        c12=distance(self.p1,self.p2)
        s12=0.5*(a12+b12+c12)
        A12=np.sqrt(s12*(s12-a12)*(s12-b12)*(s12-c12))
        
        a23=distance(self.p2,P)
        b23=distance(self.p3,P)
        c23=distance(self.p2,self.p3)
        s23=0.5*(a23+b23+c23)
        A23=np.sqrt(s23*(s23-a23)*(s23-b23)*(s23-c23))
        
        a34=distance(self.p3,P)
        b34=distance(self.p4,P)
        c34=distance(self.p3,self.p4)
        s34=0.5*(a34+b34+c34)
        A34=np.sqrt(s34*(s34-a34)*(s34-b34)*(s34-c34))
        
        a41=distance(self.p4,P)
        b41=distance(self.p1,P)
        c41=distance(self.p4,self.p1)
        s41=0.5*(a41+b41+c41)
        A41=np.sqrt(s41*(s41-a41)*(s41-b41)*(s41-c41))
        
        Atris=A12+A23+A34+A41
        
        a123=distance(self.p1,self.p2)
        b123=distance(self.p2,self.p3)
        c123=distance(self.p3,self.p1)
        s123=0.5*(a123+b123+c123)
        A123=np.sqrt(s123*(s123-a123)*(s123-b123)*(s123-c123))
        
        a134=distance(self.p1,self.p3)
        b134=distance(self.p3,self.p4)
        c134=distance(self.p4,self.p1)
        s134=0.5*(a134+b134+c134)
        A134=np.sqrt(s134*(s134-a134)*(s134-b134)*(s134-c134))

        Arect=A123+A134
        
        if abs(Atris-Arect)<0.000001:
            return True
        else:
            return False

    def rotate(self,alpha):
        """Rotation around the origin with alpha (deg)"""
        return Rectangle(self.p1.rotate(alpha),self.p2.rotate(alpha),self.p3.rotate(alpha),self.p4.rotate(alpha))

    def intersection(self,seg):
        inters=[]
        inter12=seg.intersection(self.p1p2)
        if len(inter12)>0:
            inters.append(inter12[0])
        inter23=seg.intersection(self.p2p3)
        if len(inter23)>0:
            notPresent=True
            if inter23[0].isEqual(self.p2p3.p) or inter23[0].isEqual(self.p2p3.q): #if the segment passes through the vertex, it will be encountered twice.
                for inter in inters:                                               #no need to check for the first element
                    if inter.isEqual(inter23[0]):
                        notPresent=False
            if notPresent:
                inters.append(inter23[0])
        inter34=seg.intersection(self.p3p4)
        if len(inter34)>0:
            notPresent=True
            if inter34[0].isEqual(self.p3p4.p) or inter34[0].isEqual(self.p3p4.q): #if the segment passes through the vertex, it will be encountered twice.
                for inter in inters:
                    if inter.isEqual(inter34[0]):
                        notPresent=False
            if notPresent:
                inters.append(inter34[0])
        inter41=seg.intersection(self.p4p1)
        if len(inter41)>0:
            notPresent=True
            if inter41[0].isEqual(self.p4p1.p) or inter41[0].isEqual(self.p4p1.q): #if the segment passes through the vertex, it will be encountered twice.
                for inter in inters:                                               
                    if inter.isEqual(inter41[0]):
                        notPresent=False
            if notPresent:
                inters.append(inter41[0])
        
        if len(inters)>2:
            raise ValueError('seems to be an error, more than two intersections --> concave')
            #this should not happen, since in Rectangle() I check for concave case
        else:
            return inters
            
