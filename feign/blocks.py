#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:12:45 2019

@author: zsolt
"""

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

def readMu(path,column,energy):
    """File to read attenuaton coefficients from XCOM datafiles.
    Inputs:
        path: path to the file (str)
        column: column which contains the total attenuation coefficients in case more columns are present
        energy: a list of floats or a float at which energies the coefficients are needed.
    Returns either a list of floats or a float, the interpolated value(s) of the attenuaton coefficient.
    """
    try:
        inputfile=open(path,'r').readlines()
    except FileNotFoundError:
        inputfile=open(os.getcwd()+path,'r').readlines()
    en=[]
    mu=[]
    for line in inputfile:
        x=line.strip().split()
        if len(x)>=1 and isFloat(x[0]):
            en.append(float(x[0]))
            mu.append(float(x[column]))
    return np.interp(energy,en,mu)


def is_hex_color(input_string): 
    """Function to assess whether a string is hex color description.
    Taken from https://stackoverflow.com/questions/42876366/check-if-a-string-defines-a-color
    Input: str
    Returns boolean
    """
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
    def __init__(self,*argv):
        """Define a Materials() object, which is a storage of Material() objects.
        Input: Material() objects
        Attribute: Materials().materials, a dictionary storing the Material() objects.
        >>> uox=Material('1')
        >>> zr=Material('2')
        >>> materials=Materials(uox,zr)
        >>> materials.materials
        {'1': Material(matID=1), '2': Material(matID=2)}
        """
        self.materials={}
        for arg in argv:
            if  not isinstance(arg,Material):
                raise TypeError('Inputs need to be Material() objects')
            elif arg.matID in self.materials:
                raise ValueError('matID {} is duplicated'.format(arg.matID))
            else:
                self.materials[arg.matID]=arg
        

    def __repr__(self):
        return "Materials() for collecting Material() objects"
        
    
    def add(self,material):
        """Function to add a Material() object to a Materials() object.
        Input: Materials() and Material() object
        >>> uox=Material('1')
        >>> zr=Material('2')
        >>> materials=Materials()
        >>> materials.materials
        {}
        >>> materials.add(uox)
        >>> materials.add(zr)
        >>> materials.materials
        {'1': Material(matID=1), '2': Material(matID=2)}
        """
        if isinstance(material,Material):
            if material.matID in self.materials:
                raise ValueError('matID already present in the object')
            else:
                self.materials[material.matID]=material
        else:
            raise TypeError('This is not a Material()')
    
    def remove(self,material):
        """Function to remove a Material() object from a Materials() object.
        Input: Materials() and Material() object
        Only previously added Material() objects can be removed
        >>> uox=Material('1')
        >>> zr=Material('2')
        >>> materials=Materials([fuel,clad])
        >>> materials.materials
        {'1': Material(matID=1), '2': Material(matID=2)}
        >>> materials.remove(zr)
        >>> materials.materials
        {'1': Material(matID=1)}
        >>> materials.remove(zr)
        You can remove only existing Material()
        >>> a=Point(3,4)
        >>> materials.remove(a)
        You can remove only Material()
        """
        try:
            del self.materials[material.matID]
        except AttributeError:
            print('You can remove only Material()')
        except KeyError:
            print('You can remove only existing Material()')


class Pin(object):
    def __init__(self,pinID=None):
        """Creates a new Pin() object.
        Input: pinID
        With the self.add_region() function coaxial circles can be  added to describe
        the content (eg. fuel rod, helium gap, clad).
        In case no region is added, the Pin() object will behave as an empty channel
        filled with the coolant material.
        """
        self.pinID=pinID
        self._regions=[]
        self._materials=[]
        self._radii=[]
        if pinID is None or type(pinID) is not str:
            raise ValueError('pinID has to be defined')
        
    def __repr__(self):
        return "Pin(pinID=%s)" % (self.pinID)
    
    @property
    def regions(self):
        return self._regions
    
    def add_region(self,material=None,radius=None): 
        """Function to add coaxial circles and circle rings to a pin.
        Input: Material() and radius
        In case of consecutive calls (ie. more regions added), the radii has to
        increase.
        Example, common PWR rod:
        >>> uo2 = Material('1')
        >>> he = Material('2')
        >>> zr = Material('3')
        >>> fuel = Pin('1')
        >>> fuel.add_region(uo2,0.41)
        >>> fuel.add_region(he,0.42)
        >>> fuel.add_region(zr,0.48)
        """
        if isinstance(material,Material):
            self._materials.append(material.matID)
        else:
            raise TypeError('Material() object is expected')
            
        if isFloat(radius):
            if len(self._radii)>0 and self._radii[-1]>=radius:
                raise ValueError('Radii are not increasing in pin #{}'.format(self.pinID))
            else:
                self._radii.append(radius)
        
        self._regions.append((material,radius))        

class Pins(object):
    def __init__(self,*argv):
        """Define a Pins() object, which is a storage of Pin() objects.
        Input: Pin() objects
        Attribute: Pins().pins, a dictionary storing the Pin() objects.
        >>> fuel=Pin('1')
        >>> guide=Pin('2')
        >>> pins=Pins(fuel,guide)
        >>> pins.pins
        {'1': Pin(pinID=1), '2': Pin(pinID=2)}
        """
        self.pins={}
        for arg in argv:
            if  not isinstance(arg,Pin):
                raise TypeError('Inputs need to be Pin() objects')
            elif arg.pinID in self.pins:
                raise ValueError('pinID {} is duplicated'.format(arg.pinID))
            else:
                self.pins[arg.pinID]=arg
        

    def __repr__(self):
        return "Pins() for collecting Pin() objects"
        
    
    def add(self,pin):
        """Function to add a Pin() object to a Pins() object.
        Input: Pins() and Pin() object
        >>> fuel=Pin('1')
        >>> guide=Pin('2')
        >>> pins=Pins()
        >>> pins.pins
        {}
        >>> pins.add(fuel)
        >>> pins.add(guide)
        >>> pins.pins
        {'1': Pin(pinID=1), '2': Pin(pinID=2)}
        """
        if isinstance(pin,Pin):
            if pin.pinID in self.pins:
                raise ValueError('pinID already present in the object')
            else:
                self.pins[pin.pinID]=pin
        else:
            raise TypeError('This is not a Pin()')
    
    def remove(self,pin):
        """Function to remove a Pin() object from a Pins() object.
        Input: Pins() and Pin() object
        Only previously added Pin() objects can be removed
        >>> fuel=Pin('1')
        >>> guide=Pin('2')
        >>> pins=Pins(fuel,guide)
        >>> pins.pins
        {'1': Pin(pinID=1), '2': Pin(pinID=2)}
        >>> pins.remove(guide)
        >>> pins.pins
        {'1': Pin(pinID=1)}
        >>> pins.remove(guide)
        You can remove only existing Pin()
        >>> a=Point(3,4)
        >>> pins.remove(a)
        You can remove only Pin()
        """
        try:
            del self.pins[pin.pinID]
        except AttributeError:
            print('You can remove only Pin()')
        except KeyError:
            print('You can remove only existing Pin()')

class Assembly(object):
    def __init__(self,N,M):
        """Function to initialize Assembly() objects.
        Inputs: N,M number of positions in y and x direction in the Assembly.
                N,M is converted to in if possible.
        """
        try:
            self.N=int(N)
            self.M=M
        except ValueError:
            raise ValueError('N,M has to be decimal')
        except TypeError:
            raise TypeError('N,M has to be int')
        self._pitch=None
        self._pins=None
        self._fuelmap=None
        self._coolant=None
        self._surrounding=None
        self._source=None
        self._pool=None

    def __repr__(self):
        return "Assembly(N=%d,M=%d)" % (self.absID)
    
    @property
    def pitch(self):
        return self._pitch
    
    @property
    def pool(self):
        return self._pool
    
    @property
    def pins(self):   
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
            raise TypeError('Pitch has to be float')
            
    def set_pins(self,pins):
        if isinstance(pins,Pins):
            self._pins=pins
        else:
            raise TypeError('Pins() object expected')

    def set_fuelmap(self,fuelmap=None):
        fuelmap=np.array(fuelmap)
        if  fuelmap.shape[0] != self.N or fuelmap.shape[1] != self.M:
            raise ValueError('Fuelmap has wrong size')
        else:
            self._fuelmap=fuelmap
    
    def set_coolant(self, coolant=None):
        if isinstance(coolant, Material):
            self._coolant=coolant.matID
        else:
            raise TypeError('Material() is expected')
            

            
    def set_surrounding(self, surrounding=None):
        if isinstance(surrounding, Material):
            self._surrounding=surrounding.matID
        else: 
            raise TypeError('Material() is expected')
            
            
    def set_source(self, *args):
#        if source not in Material.materials:
#            raise ValueError('Source material not defined')
#        else: 
        self._source=[]
        for arg in args:
            if isinstance(arg,Material):
                self._source.append(arg.matID)
            
    def set_pool(self,pool=None):
        if isinstance(pool,Rectangle):
            self._pool=pool
        else:
            raise TypeError('Pool has to be a Rectangle() object')
            
    def checkComplete(self):
        """Function to check whether everything is defined correctly in an 
           Assembly() object.
           - checks whether any attribute is not defined (pool does not need to be defined)
           - checks whether any pin contains any region with radius greater than
             the pitch
           - checks whether all the pins in the fuelmap are attributed to the assembly
           - in case a pool is defined, it is checked whether the pool is around the assembly.
           Returns False and print an error message otherwise.
        """
        if self.pins is None or self.pitch is None or \
           self.coolant is None or self.fuelmap is None or \
           self.source is None:                
            print('ERROR: Assembly is not complete.')
            return False
        else: 
            if False in [r<=self.pitch/2 for pin in self.pins.pins.values() for r in pin._radii]:
                print('ERROR: in a Pin() a radius is greater than the pitch')
                return False
            
            if [] in [pin._radii for pin in self.pins.pins.values()]:
                print('Warning: a pin has no regions, considered as coolant channel')
                
            if False in [self.fuelmap[i][j] in self.pins.pins for i in range(self.N) for j in range(self.M)]:
                #        elif sum(np.isin(fuelmap.flatten(),list(Pin.pins)))<self.N*self.M:
                print('ERROR: Assembly().fuelmap contains pin not included in Assembly.Pins()')
                return False
                
            if self.pool is None:
                print('Warning: no pool in the problem, the surrounding of the Assembly is filled with coolant material')
                self._accommat=self._coolant
                return True
            else:
                if self.surrounding is None:
                    print('ERROR: Surrounding material has to be defined if pool is defined')
                    return False
                else: #Check that the pool is around the fuel assembly
                    pooldummy=Rectangle(Point(self.N*self.pitch/2,self.M*self.pitch/2),
                            Point(self.N*self.pitch/2,-self.M*self.pitch/2),
                            Point(-self.N*self.pitch/2,-self.M*self.pitch/2),
                            Point(-self.N*self.pitch/2,self.M*self.pitch/2))
                    for corner in [self.pool.p1,self.pool.p2,self.pool.p3,self.pool.p4]:
                        if pooldummy.encloses_point(corner):
                            print('ERROR: Pool is inside fuel')
                            return False
                    if len(pooldummy.intersection(self.pool.p1p2))>1 or \
                          len(pooldummy.intersection(self.pool.p2p3))>1 or \
                          len(pooldummy.intersection(self.pool.p3p4))>1 or \
                          len(pooldummy.intersection(self.pool.p4p1))>1:
                        print('ERROR: Assembly does not fit in pool')
                        return False
                    else:
                        return True        

            
class Detector(object):
    def __init__(self,detID=None):
        self.detID=detID
        self._location=None
        self._collimator=None
        if detID is None:
            raise ValueError('detID has to be defined')
            
    def __repr__(self):
        return "Detector(detID=%s)" % (self.detID)
        
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
            raise TypeError('Detector location has to be Point() object')

    def set_collimator(self,collimator=None):
        if isinstance(collimator,Collimator):
            self._collimator=collimator
        else:
            raise TypeError('Collimator has to be Collimator() object')

class Detectors(object):
    def __init__(self,*argv):
        """Define a Detectors() object, which is a storage of Detector() objects.
        Input: Detector() objects
        Attribute: Detectors().detectors, a dictionary storing the Detector() objects.
        >>> F5=Detector('F5')
        >>> F15=Detector('F15')
        >>> detectors=Detectors(F5,F15)
        >>> detectors.detectors
        {'F5': Detector(detID=F5), 'F15': Detector(detID=F15)}
        """
        self.detectors={}
        for arg in argv:
            if  not isinstance(arg,Detector):
                raise TypeError('Inputs need to be Detector() objects')
            elif arg.detID in self.detectors:
                raise ValueError('detID {} is duplicated'.format(arg.detID))
            else:
                self.detectors[arg.detID]=arg
        

    def __repr__(self):
        return "Detectors() for collecting Detector() objects"
        
    
    def add(self,detector):
        """Function to add a Detector() object to a Detectors() object.
        Input: Detectors() and Detector() object
        >>> F5=Detector('F5')
        >>> F15=Detector('F15')
        >>> detectors=Detectors()
        >>> detectors.detectors
        {}
        >>> detectors.add(F5)
        >>> detectors.add(F15)
        >>> detectors.detectors
        {'F5': Detector(detID=F5), 'F15': Detector(detID=F15)}
        """
        if isinstance(detector,Detector):
            if detector.detID in self.detectors:
                raise ValueError('detID already present in the object')
            else:
                self.detectors[detector.detID]=detector
        else:
            raise TypeError('This is not a Detector()')
    
    def remove(self,detector):
        """Function to remove a Detector() object from a Detectors() object.
        Input: Detectors() and Detector() object
        Only previously added Detector() objects can be removed
        >>> F5=Detector('F5')
        >>> F15=Detector('F15')
        >>> detectors=Detectors(F5,F15)
        >>> detectors.detectors
        {'F5': Detector(detID=F5), 'F15': Detector(detID=F15)}
        >>> detectors.remove(F15)
        >>> detectors.detectors
        {'F5': Detector(detID=F5)}
        >>> detectors.remove(F15)
        You can remove only existing Detector()
        >>> a=Point(3,4)
        >>> detectors.remove(a)
        You can remove only Detector()
        """
        try:
            del self.detectors[detector.detID]
        except AttributeError:
            print('You can remove only Detector()')
        except KeyError:
            print('You can remove only existing Detector()')
            
class Absorber(object): 
    def __init__(self,absID=None):
        self.absID=absID
        self._rectangle=None  #TODO: .form to accommodate circle
        self._form=None  #TODO: .form to accommodate circle
        self._material=None
        self._accommat=None
        if absID is None:
            raise ValueError('absID has to be defined')
        
    def __repr__(self):
        return "Absorber(absID=%s)" % (self.absID)
        
    @property
    def rectangle(self):
        return self._rectangle

    @property
    def form(self):
        return self._form

    @property
    def material(self):
        return self._material

    @property
    def accommat(self):
        return self._accommat

    def set_form(self,form=None):
        if isinstance(form,Rectangle) or isinstance(form,Circle):
            self._form=form
        else:
            raise TypeError('Absorber has to be a Rectangle or Circle object')
    
    def set_rectangle(self,rectangle=None):
        if isinstance(rectangle,Rectangle):
            self._rectangle=rectangle
        else:
            raise TypeError('Absorber has to be a Rectangle object')
            
    def set_material(self, material=None):
        if isinstance(material, Material):
            self._material=material.matID
        else:
            raise TypeError('Material() is expected')

            
    def set_accommat(self, accommat=None):
        if isinstance(accommat, Material):
            self._accommat=accommat.matID
        else:
            raise TypeError('Material() is expected')
    
class Absorbers(object):
    def __init__(self,*argv):
        """Define a Absorbers() object, which is a storage of Absorber() objects.
        Input: Absorber() objects
        Attribute: Absorbers().absorbers, a dictionary storing the Absorber() objects.
        >>> leadsheet=Absorber('leadsheet')
        >>> alusheet=Absorber('alusheet')
        >>> absorbers=Absorbers(leadsheet,alusheet)
        >>> absorbers.absorbers
        {'leadsheet': Absorber(absID=leadsheet), 'alusheet': Absorber(absID=alusheet)}
        """
        self.absorbers={}
        for arg in argv:
            if  not isinstance(arg,Absorber):
                raise TypeError('Inputs need to be Absorber() objects')
            elif arg.absID in self.absorbers:
                raise ValueError('absID {} is duplicated'.format(arg.absID))
            else:
                self.absorbers[arg.absID]=arg
        

    def __repr__(self):
        return "Absorbers() for collecting Absorber() objects"
        
    
    def add(self,absorber):
        """Function to add an Absorber() object to an Absorbers() object.
        Input: Absorbers() and Absorber() object
        >>> leadsheet=Absorber('leadsheet')
        >>> alusheet=Absorber('alusheet')
        >>> absorbers=Absorbers()
        >>> absorbers.absorbers
        {}
        >>> absorbers.add(leadsheet)
        >>> absorbers.add(alusheet)
        >>> absorbers.absorbers
        {'leadsheet': Absorber(absID=leadsheet), 'alusheet': Absorber(absID=alusheet)}
        """
        if isinstance(absorber,Absorber):
            if absorber.absID in self.absorbers:
                raise ValueError('absID already present in the object')
            else:
                self.absorbers[absorber.absID]=absorber
        else:
            raise TypeError('This is not an Absorber()')
    
    def remove(self,absorber):
        """Function to remove an Absorber() object from an Absorbers() object.
        Input: Absorbers() and Absorber() object
        Only previously added Absorber() objects can be removed
        >>> leadsheet=Absorber('leadsheet')
        >>> alusheet=Absorber('alusheet')
        >>> absorbers=Absorbers(leadsheet,alusheet)
        >>> absorbers.absorbers
        {'leadsheet': Absorber(absID=leadsheet), 'alusheet': Absorber(absID=alusheet)}
        >>> absorbers.remove(alusheet)
        >>> absorbers.absorbers
        {'leadsheet': Absorber(absID=leadsheet)}
        >>> absorbers.remove(alusheet)
        You can remove only existing Absorber()
        >>> a=Point(3,4)
        >>> absorbers.remove(a)
        You can remove only Absorber()
        """
        try:
            del self.absorbers[absorber.absID]
        except AttributeError:
            print('You can remove only Absorber()')
        except KeyError:
            print('You can remove only existing Absorber()')
    
class Collimator(object):
    def __init__(self,collID):
        self.collID=collID
        self._front=None
        self._back=None
        self._color=None

    def __repr__(self):
        return "Collimator()" 
        
    @property
    def front(self):
        return self._front

    @property
    def back(self):
        return self._back
    
    @property
    def color(self):
        return self._color
    
    def set_front(self,front=None):
        if isinstance(front,Segment):
            self._front=front
        else:
            raise TypeError('Collimator front has to be a Segment object')
    
    def set_back(self,back=None):
        if isinstance(back,Segment):
            self._back=back
        else:
            raise TypeError('Collimator back has to be a Segment object')
            
    def set_color(self, color=None):
        """Color of collimator in case the geometry is plotted.
        str '#18BA09' format
        """
        if type(color) is str and is_hex_color(color):
            self._color=color
        else:
            raise ValueError(('Color has to be hex str for Material ID="{}"'.format(self.matID)))

                        
class Experiment(object):
    def __init__(self):
        self._output=None
        self._assembly=None
        self._pins=None
        self._materials=None
        self._detectors=None
        self._absorbers=None
        self._elines=None
        self._mu=None
        self._dTmap=None
        self._contributionMap=None
        self._geomEff=None

    def __repr__(self):
        return "Experiment()"
    
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
                                                    #probably not because I may want the strings in processing as well. but this can be done while processing
    @property
    def dTmap(self):
        return self._dTmap
    
    @property
    def contributionMap(self):
        return self._contributionMap
    
    def set_output(self,output='output.dat'):
        if type(output) is str:
            self._output=output
        else:
            raise TypeError('Output filename has to be str')
    
    def set_materials(self,materials):
        """Function to assign Materials() to an Experiment()
        Input: Materials() object
        >>> uox = Material('1')
        >>> zr = Material('2')
        >>> mats = Materials(uox,zr)
        >>> experiment = Experiment()
        >>> experiment.set_materials(mats)
        >>> experiment.materials
        {'1': Material(matID=1), '2': Material(matID=2)}
        """
        if isinstance(materials,Materials):
            self._materials=materials.materials
        else:
            raise TypeError('Materials() object is expected')
    
    def set_absorbers(self,absorbers):
        """Function to assign Absorbers() to an Experiment()
        Input: Absorbers() object
        >>> leadsheet = Absorber('leadsheet')
        >>> alusheet = Absorber('alusheet')
        >>> absorbers = Absorbers(alusheet,leadsheet)
        >>> experiment = Experiment()
        >>> experiment.set_absorbers(absorbers)
        >>> experiment.absorbers
        {'alusheet': Absorber(absID=alusheet), 'leadsheet': Absorber(absID=leadsheet)}
        """
        if isinstance(absorbers,Absorbers):
            self._absorbers=absorbers.absorbers
        else:
            raise TypeError('Absorbers() object is expected')
        
    def set_detectors(self,detectors):
        """Function to assign Absorbers() to an Experiment()
        Input: Absorbers() object
        >>> F5 = Detector('F5')
        >>> F15 = Detector('F15')
        >>> detectors = Detectors(F5,F15)
        >>> experiment = Experiment()
        >>> experiment.set_detectors(detectors)
        >>> experiment.detectors
        {'F5': Detector(detID=F5), 'F15': Detector(detID=F15)}
        >>> experiment.set_detectors(F5)
        >>> experiment.detectors
        {'F5': Detector(detID=F5)}
        """
        if isinstance(detectors,Detectors):
            self._detectors=detectors.detectors
        elif isinstance(detectors,Detector):
            self._detectors=Detectors(detectors).detectors
        else:
            raise TypeError('Detectors() or Detector() object is expected')
        
        
    def set_assembly(self,assembly=None):
        """Function to assignt an Assembly() object to Experiment()
        Input: Assembly() object
        """
    
        if isinstance(assembly,Assembly):
            self._assembly=assembly
            self._pins=self._assembly.pins.pins
        else:
            raise ValueError('Assembly has to be an Assembly() object')


            
    def set_elines(self,elines=None):
        if (type(elines) is list) and (False not in [type(e) is str for e in elines]) and (False not in [isFloat(e) for e in elines]):
            self._elines=elines
        else:
            raise ValueError('elines has to be a list of str MeV values')
            
    def get_MuTable(self):
        """Creates a nested dictionary to hold the attenuation coefficients.
        Outer keys are the energies, inner keys are the materials"""
        mu={e: {m: 0 for m in self.materials} for e in self._elines}
         
        for m in self.materials:
            mum=readMu(self.materials[m].path[0],self.materials[m].path[1],self.elines)
            for ei,mui in zip(self._elines,mum):
                mu[ei][m]=mui
                
        self._mu=mu
#        OLD, nicer but more file reading.
#        for e in self._elines:
#            mu[e]={key: readMu(self.materials[key].path[0],self.materials[key].path[1],float(e)) for key in self.materials}
#        self._mu=mu

            
    def distanceTravelled(self,detector):
        dTmap={key: [[0 for i in range(self.assembly.N)] for j in range(self.assembly.M)] for key in self.materials}  
        #create distance seen maps for each material
        p=self.assembly.pitch/2
        N=self.assembly.N
        M=self.assembly.M
        for i in range(N):
            for j in range(M):
                sourceIn=[s in self.pins[self.assembly.fuelmap[i][j]]._materials for s in self.assembly.source]
                if True in sourceIn: 
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
                                        for r,mat in zip(self.pins[self.assembly.fuelmap[ii][jj]]._radii, self.pins[self.assembly.fuelmap[ii][jj]]._materials): 
                                            intersects = Circle(centerShield,r).intersection(segmentSourceDetector)
                                            D=Point.distance(intersects[0],centerSource) 
                                            dT[mat]=dT[mat]+(D-Dprev)
                                            Dprev=D
                                    else:
                                        Dprev=0
                                        for r,mat in zip(self.pins[self.assembly.fuelmap[ii][jj]]._radii, self.pins[self.assembly.fuelmap[ii][jj]]._materials): 
                                            intersects = Circle(centerShield,r).intersection(segmentSourceDetector)
                                            if len(intersects)>1: #if len()==1, it is tangent, no distance traveled
                                                D=Point.distance(intersects[0],intersects[1])
                                                dT[mat]=dT[mat]+(D-Dprev)
                                                Dprev=D                                        
                                            
                        ###Distance traveled outside the pool = distance of ray-pool intersect and detector
                        if self.assembly.pool is not None:
                            dT[self.assembly.surrounding]=dT[self.assembly.surrounding]+Point.distance(self.assembly.pool.intersection(segmentSourceDetector)[0],detector.location)
                        
                        ###Distance traveled in coolantMat = total source-detector distance - everything else
                        dT[self.assembly.coolant]=dT[self.assembly.coolant]+Point.distance(centerSource,detector.location)-sum([dT[k] for k in dT.keys()])  #in case there is a ring filled with the coolent, eg an empty control rod guide, we need keep that
                        
                        ###Distance traveled in absorbers
                        ###Absorber can be Circle() or Rectangular, the syntax
                        ###is the same regarding .intersection(), thus the code
                        ###handles both as it is. 
                        for absorber in self.absorbers.values():
                            intersects=absorber.form.intersection(segmentSourceDetector)
                            if len(intersects)>1:
                                dabs=Point.distance(intersects[0],intersects[1])
                            else: #TODO if detector or source is within absorber?? elif absorber.rectangle.encloses_point(detector)
                                dabs=0
                            dT[absorber.material]=dT[absorber.material]+dabs
                            dT[absorber.accommat]=dT[absorber.accommat]-dabs
                        #Update the map
                        for key in dT:
                            dTmap[key][i][j]=dT[key]
                    else: #not through collimator
                        for key in dT:
                            dTmap[key][i][j]=np.Inf
        return dTmap
    
    def attenuation(self,dTmap,mue,detector):
        contribmap=[[0 for i in range(self.assembly.N)] for j in range(self.assembly.M)]
        p=self.assembly.pitch/2
        N=self.assembly.N
        M=self.assembly.M
        for i in range(self.assembly.N):
            for j in range(self.assembly.M):
                center=Point(-p*(N-1)+j*2*p,p*(N-1)-i*2*p)
                sourceIn=[s in self.pins[self.assembly.fuelmap[i][j]]._materials for s in self.assembly.source]
                if True in sourceIn:
                    contrib=1 #TODO might be a place to include a pre-known emission weight map. Or to provide a function which multiplies the contribution with some weight matrix
                    for key in self.materials.keys():
                        contrib=contrib*math.exp(-1*mue[key]*dTmap[key][i][j])
                    contribmap[i][j]=contrib/(4*math.pi*(Point.distance(center,detector.location))**2)
        return contribmap
    
#    def _checkData(self):
#        CHECK COLLIMATORS DONT CROSS EACHOTHER. if there is back, needs to be a front.
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
    
    def Plot(self,out=None,dpi=600,xl=[-100,100],yl=[-100,100],detectorSize=0.4):
        """Function to plot the geometry of an Experiment() object.
           The function will randomly set colors to Material() objects for which colors
           were previously not defined.
           Inputs:
               out: name of output file (str, default:None)
               dpi: set the dpi (int, default:600)
               xl,yl: region of the geometry to plot in cms (default:xl=[-100,100],yl=[-100,100]) 
               detectorSize: radius of white circle illustrating the detector points. (default:0.4)
        """
        import random
        import matplotlib.pyplot as plt        
        for mat in self.materials:
            if self.materials[mat].color is None:
                self.materials[mat].set_color("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
        
        pool=self.assembly.pool
        N=self.assembly.N
        M=self.assembly.M
        p=self.assembly.pitch/2
        fig, ax = plt.subplots()
        ax.patch.set_facecolor(self.materials[self.assembly.surrounding].color)
        if self.assembly.pool is not None:
            pool=self.assembly.pool
            polygon = plt.Polygon([[pool.p1.x,pool.p1.y],[pool.p2.x,pool.p2.y],[pool.p3.x,pool.p3.y],[pool.p4.x,pool.p4.y]], True,color=self.materials[self.assembly.coolant].color)
            ax.add_artist(polygon)
        #fuelmap
        for i in range(N):
            for j in range(M):
                center=[-p*(N-1)+j*2*p,p*(N-1)-i*2*p]
                for r,m in zip(reversed(self.pins[self.assembly.fuelmap[i][j]]._radii),reversed(self.pins[self.assembly.fuelmap[i][j]]._materials)): 
                    circle1 = plt.Circle((center[0], center[1]), r, color=self.materials[m].color)
                    ax.add_artist(circle1)
        for a in self.absorbers:
            absorber=self.absorbers[a]
            if isinstance(absorber.form,Rectangle):
                polygon = plt.Polygon([[absorber.form.p1.x,absorber.form.p1.y],[absorber.form.p2.x,absorber.form.p2.y],[absorber.form.p3.x,absorber.form.p3.y],[absorber.form.p4.x,absorber.form.p4.y]], True,color=self.materials[absorber.material].color)
                ax.add_artist(polygon)
            else:
                circle1 = plt.Circle((absorber.form.c.x,absorber.form.c.y),absorber.form.r,color=self.materials[absorber.material].color)
                ax.add_artist(circle1)
        for d in self.detectors:
            circle1= plt.Circle((self.detectors[d].location.x,self.detectors[d].location.y),detectorSize,color='white')
            ax.add_artist(circle1)
            if self.detectors[d].collimator is not None:
                if self.detectors[d].collimator.color is None:
                    self.detectors[d].collimator.set_color('#C2C5CC')
                #the "orientation" of back and front is not know, so I plot two ways.
                polygon=plt.Polygon([[self.detectors[d].collimator.front.p.x,self.detectors[d].collimator.front.p.y],[self.detectors[d].collimator.front.q.x, self.detectors[d].collimator.front.q.y],[self.detectors[d].collimator.back.p.x,self.detectors[d].collimator.back.p.y],[self.detectors[d].collimator.back.q.x,self.detectors[d].collimator.back.q.y]],True,color=self.detectors[d].collimator.color)
                ax.add_artist(polygon)
                polygon=plt.Polygon([[self.detectors[d].collimator.front.p.x,self.detectors[d].collimator.front.p.y],[self.detectors[d].collimator.front.q.x, self.detectors[d].collimator.front.q.y],[self.detectors[d].collimator.back.q.x,self.detectors[d].collimator.back.q.y],[self.detectors[d].collimator.back.p.x,self.detectors[d].collimator.back.p.y]],True,color=self.detectors[d].collimator.color)
                ax.add_artist(polygon)
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

        if self._elines is not None:  #TODO if i check this elsewhere, can be removed or NO, because in that case maybe just the distance travelled is of interest.      
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
                        sourceIn=[s in self.pins[self.assembly.fuelmap[i][j]]._materials for s in self.assembly.source]
                        if True in sourceIn:
                            counts=counts+contributionMapAve[e][i][j]
                            sourceNorm=sourceNorm+1
                counts=counts/sourceNorm #TODO do i actually wanna normalize with the number of pins?
                geomefficiency.append(counts) #TODO calc_geomEff(contribMapAve)???
    
            self._contributionMap=contributionMapAve
            self._geomEff=geomefficiency
            if self.output is not None:
                output=open(self.output,'w')
                for e,c in zip(self._elines,self._geomEff):
                    output.write(e+'\t'+str(c)+'\n')
                output.close()
        
#        self._dTmap[detector.detID]=dTmap
                            

        