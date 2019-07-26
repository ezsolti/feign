#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:12:45 2019

@author: zsolt
"""

#TODO load test data!!!

import os
import numpy as np
import math
import re
import matplotlib.pyplot as plt
from feign.geometry import *


def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def readMu(path,column,energy): #TODO restructure somehow
    inputfile=open(os.getcwd()+path,'r').readlines()
    en=[]
    mu=[]
    for line in inputfile:
        x=line.strip().split()
        if len(x)>=1 and isFloat(x[0]):
            en.append(float(x[0]))
            mu.append(float(x[column]))
    return np.interp(energy,en,mu)


def is_hex_color(input_string): #from https://stackoverflow.com/questions/42876366/check-if-a-string-defines-a-color
    HEX_COLOR_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    regexp = re.compile(HEX_COLOR_REGEX)
    if regexp.search(input_string):
        return True
    return False


class Material(object):
    '''Creates a new material object'''
    def __init__(self, matID=None):
        '''Defines name, id, density and data path'''
        self.matID = matID
        self._density = None
        self._path = None
        self._data = None #todo to preload data?!
        self._color = None
        if matID is None or type(matID) is not str:
            raise ValueError('matID has to be defined with a string')

    def __repr__(self):
        return "Material(matID=%s)" % (self.matID)

    @property
    def density(self):
        return self._density
    
    @property
    def path(self):
        return self._path
    
    @property
    def color(self):
        return self._color

    def set_density(self, density=None):
        """Set the density of the material
        density : float in g/cm2
        """
        
        if isFloat(density):
            self._density=density
        else:
            raise ValueError('density has to be float for Material ID="{}"'.format(self.matID))
            
    def set_path(self, path=None):
        """Path to the attenuation data of the Material:
            (str,int) tuple, str to describe path, int to describe column needed.
        """
        if type(path) is tuple and len(path)==2 and type(path[0]) is str and type(path[1]) is int:
            self._path=path
        else:
            raise ValueError(('Path has to be (str,int) tuple for Material ID="{}"'.format(self.matID)))
            
    def set_color(self, color=None):
        """Color of material in case the geometry is plotted.
        str '#18BA09' format
        """
        if type(color) is str and is_hex_color(color):
            self._color=color
        else:
            raise ValueError(('Color has to be hex str for Material ID="{}"'.format(self.matID)))
            

class Materials(object):
    def __init__(self,materials=[]):
        if type(materials) is not list:
            raise ValueError('Materials() expects a list of materials')
        elif False in [isinstance(m,Material) for m in materials]:
            raise ValueError('A material is not a Material() object')
        elif len([m.matID for m in materials])-len(set([m.matID for m in materials]))!=0:
            raise ValueError('Some materials have the same matID')
        else:
            self.materials={mat.matID: mat for mat in materials}
        

    def __repr__(self):
        return "Materials() for collecting Material() objects"
        
    
    def add(self,material):
        if isinstance(material,Material):
            if material.matID in self._materialsdict:
                raise ValueError('matID already present in the object')
            else:
                self.materials[material.matID]=material #TODO do I need to keep the list?
        else:
            raise ValueError('This is not a Material()')

    def remove(self,material): #TODO, wrong
        try:
            del self.materialsdict[material.matID]
        except AttributeError:
            print('You can remove only Material()')
        except KeyError:
            print('You can remove only existing Material()')
        
        
class Pin(object):
    """creates a new cell"""
    def __init__(self,pinID=None):
        self.pinID=pinID
        self._regions=[]   #TODO make it None???
        self._materials=[]
        self._radii=[]
        if pinID is None or type(pinID) is not str:
            raise ValueError('pinID has to be defined')
        
    
    @property
    def regions(self):
        return self._regions
        
    def add_region(self,region=(0,None)): #TODO what if r is bigger than p/2?? where to check? in assy
        if len(self._regions)>0 and self._regions[-1][0]>=region[0]: #TODO add pin through variable
            raise ValueError('Radii are not increasing in cell #{}'.format(self.pinID))
#        elif region[1] not in Material.materials:
#            raise ValueError('Material does not exist')  TODO: such a check when pins are added to experiment
        else:
            self._regions.append(region)
            self._radii.append(region[0])
            self._materials.append(region[1])

class Pins(object):
    def __init__(self,pins=[]):
        if type(pins) is not list:
            raise ValueError('Pins() expects a list of pins')
        elif False in [isinstance(p,Pin) for p in pins]:
            raise ValueError('A pin is not a Pin() object')
        elif len([p.pinID for p in pins])-len(set([p.pinID for p in pins]))!=0:
            raise ValueError('Some pins have the same pinID')
        else:
            self.pins={pin.pinID: pin for pin in pins}
        

    def __repr__(self):
        return "Pins() for collecting Pin() objects"
        
    
    def add(self,pin):
        if isinstance(pin,Pin):
            if pin.pinID in self._pinsdict:
                raise ValueError('pinID already present in the object')
            else:
                self.pins[pin.pinID]=pin
        else:
            raise ValueError('This is not a Pin()')

    def remove(self,pin): #TODO, wrong
        try:
            del self.pinsdict[pin.pinID]
        except AttributeError:
            print('You can remove only Pin()')
        except KeyError:
            print('You can remove only existing Pin()')

class Assembly(object):
    def __init__(self,N,M): #No need for N and M? set it separately?
        self.N=N
        self.M=M
        self._pitch=None
        self._pins=None
        self._fuelmap=None
        #self._materials
        self._coolant=None
        self._surrounding=None
        self._source=None
        self._pool=None
        
    @property
    def pitch(self):
        return self._pitch
    
    @property
    def pool(self):
        return self._pool
    
    @property
    def pins(self):   #TODO now this is both in experiment and here
        return self._pins
    
    @property
    def fuelmap(self):
        return self._fuelmap

    @property
    def coolant(self):
        return self._coolant
    
    @property
    def surrounding(self):
        return self._surrounding

    @property
    def source(self):
        return self._source

    
    def set_pitch(self,pitch=None):
        if isFloat(pitch):
            self._pitch=pitch
        else:
            raise ValueError('Pitch has to be float')
            
    def set_pins(self,pins):
        if isinstance(pins,Pins):
            self._pins=pins
        else:
            raise TypeError('Pins() object expected')

    def set_fuelmap(self,fuelmap=None):
        fuelmap=np.array(fuelmap)
        if  fuelmap.shape[0] != self.N or fuelmap.shape[1] != self.M:
            raise ValueError('Fuelmap has wrong size')
#        elif sum(np.isin(fuelmap.flatten(),list(Pin.pins)))<self.N*self.M:
#            raise ValueError('Pin cell not defined')  TODO: check this in experiment!!!
        else:
            self._fuelmap=fuelmap
    
    def set_coolant(self, coolant=None):
#        if coolant not in Material.materials:
#            raise ValueError('Coolant material not defined')
#        else: 
        self._coolant=coolant

            
    def set_surrounding(self, surrounding=None):
#        if surrounding not in Material.materials:
#            raise ValueError('Surrounding material not defined')
#        else: 
        self._surrounding=surrounding
            
    def set_source(self, source=None):
        if source not in Material.materials:
            raise ValueError('Source material not defined')
        else: 
            self._source=source
            
    def set_pool(self,pool=None):
        if isinstance(pool,Rectangle):
            self._pool=pool
        else:
            raise ValueError('Pool has to be a Rectangle object')
            
class Detector(object):
    def __init__(self,detID=None):
        self.detID=detID
        self._location=None
        self._collimator=None
        if detID is None:
            raise ValueError('detID has to be defined')
        
    @property
    def location(self):
        return self._location

    @property
    def collimator(self):
        return self._collimator
    
    def set_location(self,location=None):
        if isinstance(location,Point):
            self._location=location
        else:
            raise ValueError('Detector location has to be Point object')

    def set_collimator(self,collimator=None):
        if isinstance(collimator,Collimator):
            self._collimator=collimator
        else:
            raise ValueError('Detector location has to be Point object')

class Detectors(object):
    def __init__(self,detectors=[]):
        if type(detectors) is not list:
            raise ValueError('Detectors() expects a list of detectors')
        elif False in [isinstance(p,Detector) for p in detectors]:
            raise ValueError('A detector is not a Detector() object')
        elif len([d.detID for d in detectors])-len(set([d.detID for d in detectors]))!=0:
            raise ValueError('Some detectors have the same detID')
        else:
            self.detectors={detector.detID: detector for detector in detectors}
        

    def __repr__(self):
        return "Detectors() for collecting Detector() objects"
        
    
    def add(self,detector):
        if isinstance(detector,Detector):
            if detector.detectorID in self._detectorsdict:
                raise ValueError('detectorID already present in the object')
            else:
                self.detectors[detector.detectorID]=detector
        else:
            raise ValueError('This is not a Detector()')

    def remove(self,detector): #TODO, wrong
        try:
            del self.detectorsdict[detector.detectorID]
        except AttributeError:
            print('You can remove only Detector()')
        except KeyError:
            print('You can remove only existing Detector()')
            
class Absorber(object): #TODO: absorber sets might be attributed to Detectors
    def __init__(self,absID=None):
        self.absID=absID
        self._rectangle=None
        self._material=None
        self._accommat=None
        if absID is None:
            raise ValueError('absID has to be defined')
        
            
    @property
    def rectangle(self):
        return self._rectangle

    @property
    def material(self):
        return self._material

    @property
    def accommat(self):
        return self._accommat
    
    def set_rectangle(self,rectangle=None):
        if isinstance(rectangle,Rectangle):
            self._rectangle=rectangle
        else:
            raise ValueError('Absorber has to be a Rectangle object')
            
    def set_material(self, material=None):
#        if material not in Material.materials:
#            raise ValueError('Absorber material not defined')
#        else: 
        self._material=material

            
    def set_accommat(self, accommat=None):
#        if accommat not in Material.materials:
#            raise ValueError('Accommodating material not defined')
#        else:
        self._accommat=accommat
    #TODO: check that material is available in Experiment        
    #TODO: a way to check whether no place is duplicated
    
class Absorbers(object):
    def __init__(self,absorbers=[]):
        if type(absorbers) is not list:
            raise ValueError('Absorbers() expects a list of absorbers')
        elif False in [isinstance(p,Absorber) for p in absorbers]:
            raise ValueError('One absorber is not a Absorber() object')
        elif len([a.absID for a in absorbers])-len(set([a.absID for a in absorbers]))!=0:
            raise ValueError('Some absorbers have the same detID')
        else:
            self.absorbers={absorber.absID: absorber for absorber in absorbers}
        

    def __repr__(self):
        return "Absorbers() for collecting Absorber() objects"
        
    
    def add(self,absorber):
        if isinstance(absorber,Absorber):
            if absorber.absorberID in self._absorbersdict:
                raise ValueError('absorberID already present in the object')
            else:
                self.absorbers[absorber.absorberID]=absorber
        else:
            raise ValueError('This is not a Absorber()')

    def remove(self,absorber): #TODO, wrong
        try:
            del self.absorbersdict[absorber.absorberID]
        except AttributeError:
            print('You can remove only Absorber()')
        except KeyError:
            print('You can remove only existing Absorber()')
    
class Collimator(object):
    #collimators={}
    def __init__(self,collID):
        self.collID=collID
        self._front=None
        self._back=None
     #   if collID in Collimator.collimators:
     #       raise ValueError('Absorber "{}" already exists'.format(detID))
     #   elif detID is None:
     #       raise ValueError('absID has to be defined')
     #   else:
     #       Collimator.collimator[collID]=self
            
    @property
    def front(self):
        return self._front

    @property
    def back(self):
        return self._back
    
    def set_front(self,front=None):
        if isinstance(front,Segment):
            self._front=front
        else:
            raise ValueError('Collimator front has to be a Segment object')
    
    def set_back(self,back=None):
        if isinstance(back,Segment):
            self._back=back
        else:
            raise ValueError('Collimator back has to be a Segment object')

                        
class Experiment(object):
    def __init__(self):
        self._output=None
        self._assembly=None
        self._pins=None#Pin.pins
        self._materials=None#Material.materials
        self._detectors=None#Detector.detectors #TODO make "plural" classes
        self._absorbers=None#Absorber.absorbers
        self._elines=None
        self._mu=None
        self._dTmap=None
        self._contributionMap=None
        self._geomEff=None
        
    @property
    def output(self):
        return self._output
    
    @property
    def assembly(self):
        return self._assembly

    @property
    def cells(self):
        return self._cells

    @property
    def materials(self):
        return self._materials

    @property
    def pins(self):
        return self._pins
    
    @property
    def detectors(self):
        return self._detectors

    @property
    def absorbers(self):
        return self._absorbers

    
    @property
    def elines(self):
        return np.array(self._elines).astype(float) #TODO, i want the strings for later, but for plotting float is better. Is this a correct way to do it?

    @property
    def dTmap(self):
        return self._dTmap
    
    @property
    def contributionMap(self):
        return self.contributionMap
    
    def set_output(self,output='output.dat'):
        if type(output) is str:
            self._output=output
        else:
            raise ValueError('Output filename has to be str')
    
    def set_materials(self,materials):
        self._materials=materials.materials
    
    def set_absorbers(self,absorbers):
        self._absorbers=absorbers.absorbers #TODO
        
    def set_detectors(self,detectors):
        self._detectors=detectors.detectors #TODO
        
    def set_assembly(self,assembly=None):
        #TODO check that assemblypool doesnt cut in 17*pitch
        if isinstance(assembly,Assembly):
            if assembly.pins is None or assembly.pitch is None or \
            assembly.coolant is None or assembly.fuelmap is None or \
            assembly.pool is None or assembly.surrounding is None or assembly.source is None:
                raise ValueError('Assembly is not complete')
            else:
                self._assembly=assembly
                self._pins=assembly.pins.pins
        else:
            raise ValueError('Assembly has to be a Assembly object')

#        TODO: check that pool is not inside assembly. the stuff below just checks that they dont cross eachother       
#        pooldummy=Rectangle(Point(assembly.N*assembly.pitch/2,assembly.M*assembly.pitch/2),
#                            Point(assembly.N*assembly.pitch/2,-assembly.M*assembly.pitch/2),
#                            Point(-assembly.N*assembly.pitch/2,-assembly.M*assembly.pitch/2),
#                            Point(-assembly.N*assembly.pitch/2,assembly.M*assembly.pitch/2))
#        print(pooldummy)
#        print(assembly.pool)
#        if len(pooldummy.intersection(assembly.pool.p1p2))>1 or \
#           len(pooldummy.intersection(assembly.pool.p2p3))>1 or \
#           len(pooldummy.intersection(assembly.pool.p3p4))>1 or \
#           len(pooldummy.intersection(assembly.pool.p4p1))>1:
#            raise ValueError('Assembly does not fit in pool')
            
    def set_elines(self,elines=None):
        if (type(elines) is list) and (False not in [type(e) is str for e in elines]) and (False not in [isFloat(e) for e in elines]):
            self._elines=elines
        else:
            raise ValueError('elines has to be a list of str MeV values')
            
    def get_MuTable(self):
        """Creates a nested dictionary to hold the attenuation coefficients.
        Outer keys are the energies, inner keys are the materials"""
        mu={}
        try:
            for e in self._elines:
                mu[e]={key: readMu(self.materials[key].path[0],self.materials[key].path[1],float(e)) for key in self.materials}
            self._mu=mu
        except FileNotFoundError:
            print('The data file is not present')
        except IndexError:
            print('Not enough column in file')
            
    def distanceTravelled(self,detector):
        dTmap={key: [[0 for i in range(self.assembly.N)] for j in range(self.assembly.M)] for key in self.materials}  
        #create distance seen maps for each material
        p=self.assembly.pitch/2
        N=self.assembly.N
        M=self.assembly.M
        for i in range(N):
            for j in range(M):
                if self.assembly.fuelmap[i][j] in self.assembly.source: #TODO maybe a source material should be?
                    dT={key: 0 for key in self.materials} #dict to track distances travelled in each material for a given pin
                    
                    centerSource=Point(-p*(N-1)+j*2*p,p*(N-1)-i*2*p)
                    segmentSourceDetector=Segment(centerSource,detector.location)
                    #Only track rays which pass through the collimator
                    if detector.collimator==None or (len(detector.collimator.front.intersection(segmentSourceDetector))==1 and
                       len(detector.collimator.back.intersection(segmentSourceDetector))==1):
                       ###Distances traveled in other pin positions
                        for ii in range(N):
                            for jj in range(M):
                                centerShield=Point(-p*(N-1)+jj*2*p,p*(N-1)-ii*2*p)
                                pinChannel=Rectangle(centerShield.translate(-p,p),centerShield.translate(p,p),
                                                   centerShield.translate(p,-p),centerShield.translate(-p,-p))
                                
                                if len(pinChannel.intersection(segmentSourceDetector))>=1: #check only pins in between Source and Detector
                                    if ii==i and jj==j: #pinChannel.encloses_point(centerSource): #in that case, only one intersection
                                        Dprev=0
                                        for r,mat in zip(self.pins[self.assembly.fuelmap[ii][jj]]._radii, self.pins[self.assembly.fuelmap[ii][jj]]._materials): #TODO if pins get into assembly, then look in that
                                            intersects = Circle(centerShield,r).intersection(segmentSourceDetector)
                                            D=Point.distance(intersects[0],centerSource) 
                                            dT[mat]=dT[mat]+(D-Dprev)
                                            Dprev=D
                                    else:
                                        Dprev=0
                                        for r,mat in zip(self.pins[self.assembly.fuelmap[ii][jj]]._radii, self.pins[self.assembly.fuelmap[ii][jj]]._materials): #TODO if pins get into assembly, then look in that
                                            intersects = Circle(centerShield,r).intersection(segmentSourceDetector)
                                            if len(intersects)>1: #if len()==1, it is tangent, no distance traveled
                                                D=Point.distance(intersects[0],intersects[1])
                                                dT[mat]=dT[mat]+(D-Dprev)
                                                Dprev=D                                        
                                            
                        ###Distance traveled outside the pool = distance of ray-pool intersect and detector
                        dT[self.assembly.surrounding]=dT[self.assembly.surrounding]+Point.distance(self.assembly.pool.intersection(segmentSourceDetector)[0],detector.location)
                        
                        ###Distance traveled in coolantMat = total source-detector distance - everything else
                        dT[self.assembly.coolant]=dT[self.assembly.coolant]+Point.distance(centerSource,detector.location)-sum([dT[k] for k in dT.keys()])  #in case there is a ring filled with the coolent, eg an empty control rod guide, we need keep that
                        
                        ###Distance traveled in absorbers
                        for absorber in self.absorbers.values():
                            intersects=absorber.rectangle.intersection(segmentSourceDetector)
                            if len(intersects)>1:
                                dabs=Point.distance(intersects[0],intersects[1])
                            else:
                                dabs=0
                            dT[absorber.material]=dT[absorber.material]+dabs
                            dT[absorber.accommat]=dT[absorber.accommat]-dabs
                        
                        #Update the map
                        for key in dT:
                            dTmap[key][i][j]=dT[key]
        return dTmap
    
    def attenuation(self,dTmap,mue,detector):
        contribmap=[[0 for i in range(self.assembly.N)] for j in range(self.assembly.M)]
        p=self.assembly.pitch/2
        N=self.assembly.N
        M=self.assembly.M
        for i in range(self.assembly.N):
            for j in range(self.assembly.M):
                center=Point(-p*(N-1)+j*2*p,p*(N-1)-i*2*p)
                if self.assembly.fuelmap[i][j] in self.assembly.source:
                    contrib=1 #TODO might be a place to include a pre-known emission weight map
                    for key in self.materials.keys():
                        contrib=contrib*math.exp(-1*mue[key]*dTmap[key][i][j])
                    contribmap[i][j]=contrib/(4*math.pi*(Point.distance(center,detector.location))**2)
        return contribmap
    
#    def _checkData(self):
#        if self._assembly is None:
#            raise ValueError('Assembly has to be present in Experiment')
#        else:
#            #go through assembly mandatory attributes. pool can be the side of the assembly
#        if self._pins: #ez nagyon az assemblybe kellene!!!
#        if self._materials #now is the time to check that the pins are present in material
#        if self._detectors is None:
#            raise ValueError('At least one Detector() has to be defined')
#        if self._elines is None:
#            print('Only distance travelled in various materials will be computed')
    
    def Plot(self,out=None,dpi=600,xl=[-100,100],yl=[-100,100]):
        
        import random
        import matplotlib.pyplot as plt
#        import matplotlib.path as mpath
#        import matplotlib.lines as mlines
#        import matplotlib.patches as mpatches
#        from matplotlib.collections import PatchCollection
        
        for mat in self.materials:
            if self.materials[mat].color is None:
                self.materials[mat].set_color("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
        
        pool=self.assembly.pool
        N=self.assembly.N
        M=self.assembly.M
        p=self.assembly.pitch/2
        fig, ax = plt.subplots()
        ax.patch.set_facecolor(self.materials[self.assembly.surrounding].color)
        polygon = plt.Polygon([[pool.p1.x,pool.p1.y],[pool.p2.x,pool.p2.y],[pool.p3.x,pool.p3.y],[pool.p4.x,pool.p4.y]], True,color=self.materials[self.assembly.coolant].color)
        ax.add_artist(polygon)
        #fuelmap
        for i in range(N):
            for j in range(M):
                center=[-p*(N-1)+j*2*p,p*(N-1)-i*2*p]
                for r,m in zip(reversed(self.pins[self.assembly.fuelmap[i][j]]._radii),reversed(self.pins[self.assembly.fuelmap[i][j]]._materials)): #TODO if pins get into assembly, then look in that
                    circle1 = plt.Circle((center[0], center[1]), r, color=self.materials[m].color)
                    ax.add_artist(circle1)
        for a in self.absorbers:
            absorber=self.absorbers[a]
            polygon = plt.Polygon([[absorber.rectangle.p1.x,absorber.rectangle.p1.y],[absorber.rectangle.p2.x,absorber.rectangle.p2.y],[absorber.rectangle.p3.x,absorber.rectangle.p3.y],[absorber.rectangle.p4.x,absorber.rectangle.p4.y]], True,color=self.materials[absorber.material].color)
            ax.add_artist(polygon)
        for d in self.detectors:
            circle1= plt.Circle((self.detectors[d].location.x,self.detectors[d].location.y),0.4,color='white') #TODO, maybe dont hard code radius?
            ax.add_artist(circle1)
            #TODO collimator
        plt.xlim(xl[0],xl[1])
        plt.ylim(yl[0],yl[1])
        plt.gca().set_aspect('equal', adjustable='box')
        if out is not None:
            plt.savefig(out,dpi=dpi)
        plt.show()
        
        
    def Run(self):
        dTmap={}
        for name in self.detectors:
            print(name)
            dTmap[name]=self.distanceTravelled(self.detectors[name]) 
        self._dTmap=dTmap

        if self._elines is not None:        
            geomefficiency=[]
            contributionMapAve={}
            self.get_MuTable()
            for e in self._elines:
                print(e)
                mue=self._mu[e]
                muem={key: mue[key]*self.materials[key].density for key in mue.keys()}
                contributionMapAve[e]=[[0 for i in range(self.assembly.N)] for j in range(self.assembly.M)]
                for name in self.detectors: #this could go through dTmap as well...:)
                    contributionMap=self.attenuation(dTmap[name],muem,self.detectors[name])
                    #contributionMapAve[e]=[[contributionMapAve[e][i][j]+contributionMap[i][j] for i in range(N)] for j in range(M)]
                    for i in range(self.assembly.N):
                        for j in range(self.assembly.M):
                            contributionMapAve[e][i][j]=contributionMapAve[e][i][j]+contributionMap[i][j]/len(self.detectors)
                counts=0
                sourceNorm=0
                for i in range(self.assembly.N):
                    for j in range(self.assembly.M):
                        if self.assembly.fuelmap[i][j] in self.assembly.source:
                            counts=counts+contributionMapAve[e][i][j]
                            sourceNorm=sourceNorm+1
                counts=counts/sourceNorm #TODO do i actually wanna normalize with the number of pins?
                geomefficiency.append(counts)
    
            self._contributionMap=contributionMapAve
            self._geomEff=geomefficiency
            if self.output is not None:
                output=open(self.output,'w')
                for e,c in zip(self._elines,self._geomEff):
                    output.write(e+'\t'+str(c)+'\n')
                output.close()
        
#        self._dTmap[detector.detID]=dTmap
                            

        