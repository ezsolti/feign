#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:12:45 2019

@author: zsolt
"""

import os
import math
import re
import numpy as np
import matplotlib.pyplot as plt
from feign.geometry import *


def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def readMu(path,column,energy):
    """The function to read attenuaton coefficients from XCOM datafiles.

    Parameters
    ----------
    path : str
        path to the file (str)
    column : int
        column which contains the total attenuation coefficients in case more
        columns are present in the file
    energy : float or list of floats
        energy or energies where the attenuation coefficient is needed.

    Returns
    -------
    float or list of floats
        the interpolated value(s) of the attenuaton coefficient.
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
    """The function to assess whether a string is hex color description.

    Taken from https://stackoverflow.com/questions/42876366/check-if-a-string-defines-a-color

    Parameters
    ----------
    input_string : str
      String which may contain hex color description

    Returns
    -------
    bool
      True if the string is a hex format definition, False otherwise.

    Examples
    --------
    >>> is_hex_color('notahex')
    False
    >>> is_hex_color('#FF0000')
    True
    """
    HEX_COLOR_REGEX = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    regexp = re.compile(HEX_COLOR_REGEX)
    if regexp.search(input_string):
        return True
    return False

def getID(nameKeyword, argList, keywordDict):
    """The function returns 1 string argument from a general list or arguments

    The argument can be named with nameKeyword

    Parameters
    ----------
    nameKeyword : str
      The keyword of the desired argument if named

    argList : list
      *args passed to this function

    keywordDict : dict
      **kwargs passed to this function

    Returns
    -------
    str
      The found string argument
    """

    foundArg = None

    if len(argList) == 1 and len(keywordDict) == 0:
        foundArg = argList[0]
    elif len(argList) == 0 and len(keywordDict) == 1 and nameKeyword in keywordDict:
        foundArg = keywordDict[nameKeyword]

    if foundArg is not None and isinstance(foundArg, str):
        return foundArg

    raise ValueError('expected 1 argument: '+nameKeyword+' string')


class Material(object):
    """A class used to represent a Material.

    Parameters
    ----------
    matID : str
      ID of the material

    Attributes
    ----------
    matID : str
        ID of the material
    density : float
        density of material in (g/cm3)
    path : str
        path to attenuation coefficient file
    color : str
        color of material when plotting
    """

    _idName = 'matID'

    def __init__(self, *args, **kwargs):
        self._density = None
        self._path = None
        self._color = None
        self._id = getID(self._idName, args, kwargs)

    def __repr__(self):
        return "Material(matID=%s)" % (self._id)

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
        """The function to set the density of the Material

        Parameters
        ----------
        density : float
            density of material in g/cm2
        """

        if isFloat(density):
            self._density=density
        else:
            raise ValueError('density has to be float for Material ID="{}"'.format(self._id))

    def set_path(self, path=None):
        """The function to set the path to the attenuation data of the Material.

        Parameters
        ----------
        path : tuple (str,int)
            the path of the file, and the column which contains the data.
        """
        if isinstance(path, tuple) and len(path)==2 and isinstance(path[0], str) and isinstance(path[1], int):
            self._path=path
        else:
            raise ValueError(('Path has to be (str,int) tuple for Material ID="{}"'.format(self._id)))

    def set_color(self, color=None):
        """The function to set the color of Material in case the geometry is plotted.

        Parameters
        ----------
        color : str
            color of the material in hex format
        """
        if isinstance(color, str) and is_hex_color(color):
            self._color=color
        else:
            raise ValueError(('Color has to be hex str for Material ID="{}"'.format(self._id)))


class Pin(object):
    """A class used to represent a Pin.
    With :meth:`Pin.add_region()` coaxial circles can be  added to describe
    the content (eg. fuel pellet, helium gap, clad).
    In case no region is added, the Pin() object will behave as an empty channel
    filled with the coolant material.

    Parameters
    ----------
    pinID : str
        ID of the pin

    Attributes
    ----------
    pinID : str
        ID of the pin
    regions : list of tuples
        (Material, radius) pairs to describe coaxial regions within pin, radius in cm.
    materials : list of str
        list of :attr:`Material.matID` identifiers within the pin
    radii : list of floats
        list of radii of regions within the pin, radii in cm
    """

    _idName = 'pinID'

    def __init__(self, *args, **kwargs):
        self._regions=[]
        self._materials=[]
        self._radii=[]
        self._id = getID(self._idName, args, kwargs)

    def __repr__(self):
        return "Pin(pinID=%s)" % (self._id)

    @property
    def regions(self):
        return self._regions

    @property
    def materials(self):
        return self._materials

    @property
    def radii(self):
        return self._radii

    def add_region(self,material=None,radius=None):
        """The function to add coaxial circles and rings to a pin.
        In case of consecutive calls (ie. more regions added), the radii has to
        increase.

        Parameters
        ----------
        material : Material
            material filled into new region
        radius :
            radius of new region


        Examples
        --------
        >>> uo2 = Material('1')
        >>> he = Material('2')
        >>> zr = Material('3')
        >>> fuel = Pin('1')
        >>> fuel.add_region(uo2,0.41)
        >>> fuel.add_region(he,0.42)
        >>> fuel.add_region(zr,0.48)
        >>> fuel.regions
        [(Material(matID=1), 0.41),
         (Material(matID=2), 0.42),
         (Material(matID=3), 0.48)]
        """
        if isinstance(material,Material):
            self._materials.append(material._id)
        else:
            raise TypeError('Material() object is expected')

        if isFloat(radius):
            if len(self._radii)>0 and self._radii[-1]>=radius:
                raise ValueError('Radii are not increasing in pin #{}'.format(self._id))
            else:
                self._radii.append(radius)

        self._regions.append((material,radius))


def checkArgvConsistency(*argv):
    if len(argv) >= 2:
        for arg in argv[1:]:
            if not isinstance(arg, type(argv[0])):
                raise TypeError('Inconsistent input objects: '+str(type(arg))+' != '+str(type(argv[0])))

def addIDsToDict(objectDict, *argv):
    checkArgvConsistency(*argv)

    #add new elements
    for arg in argv:
        if arg._id in objectDict:
            raise ValueError('ID {} is duplicated'.format(arg._id))
        else:
            objectDict[arg._id]=arg

def delIDsFromDict(objectDict, *argv):
    checkArgvConsistency(*argv)

    for arg in argv:
        if objectDict is None:
            raise TypeError('No objects added yet.')
        elif arg._id in objectDict:
            print('ID {} is not in dict yet'.format(arg._id))
        else:
            del objectDict[arg._id]

class Assembly(object):
    """A class used to represent a rectangular Assembly.

    Parameters
    ----------
    N : int
        number of positions in y direction
    M : int
        number of positions in x direction

    Attributes
    ----------
    N : int
        number of positions in y direction
    M : int
        number of positions in x direction
    pitch : float
        pitch size of the lattice in cm
    pins: Pins()
        pins in the assembly
    fuelmap: 2D array
        fuelmap to describe which pins are filled in the positions
    coolant : str
        matID of the coolant (ie. materal filled between pins)
    pool : Rectangle() (optional)
        pool in which the assembly is placed. Within the pool coolant material is
        filled, outside the pool surrounding material is filled.
    surrounding : str (mandatory if pool is present)
        matID of the surrounding material (ie. material filled around pool)
    source : list of str
        :attr:`Material.matID` identifiers of material emitting gamma particles
    """
    def __init__(self,N,M):
        try:
            self.N=int(N)
            self.M=int(M)
        except ValueError:
            raise ValueError('N,M has to be decimal')
        except TypeError:
            raise TypeError('N,M has to be int')
        self._pitch=None
        self._pins=None
        self._fuelmap=None
        self._coolant=None
        self._surrounding=None
        self._source=None #TODO what if more materials emit from same pin?
        self._pool=None

    def __repr__(self):
        return "Assembly(N=%d,M=%d)" % (self.N,self.M)

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
        """The function to set the pitch of the lattice of Assembly

        Parameters
        ----------
        pitch : float
            pitch of lattice in cm
        """
        if isFloat(pitch):
            self._pitch=pitch
        else:
            raise TypeError('Pitch has to be float')

    def set_pins(self,*argv):
        """The function to include Pin objects in an Assembly

        Parameters
        ----------
        *argv : Pin() or more Pin() objects
            Pin() objects to be included in the Assembly

        Examples
        --------
        >>> fuel=Pin('1')
        >>> guide=Pin('2')
        >>> assembly=Assembly(2,2)
        >>> assembly.pins

        >>> assembly.set_pins(fuel,guide)
        >>> assembly.pins
        {'1': Pin(pinID=1), '2': Pin(pinID=2)}


        Raises
        ------
        TypeError
            if the parameter is not Pin()
        ValueError
            if the Pin is already included
        """

        self._pins={}
        self.add_pin(*argv)

    def add_pin(self,*argv):
        """The function to add Pin objects to an Assembly, which may have
        already included pins. If one wants to rewrite the existing pins,
        then the :meth:`Assembly.set_pins()` has to be called.

        Parameters
        ----------
        *argv : Pin() or more Pin() objects
            Pin() objects to be added in the Assembly

        Examples
        --------
        >>> fuel=Pin('1')
        >>> guide=Pin('2')
        >>> assembly=Assembly(2,2)
        >>> assembly.set_pins()
        >>> assembly.pins
        {}
        >>> assembly.add_pin(fuel)
        >>> assembly.add_pin(guide)
        >>> assembly.pins
        {'1': Pin(pinID=1), '2': Pin(pinID=2)}

        Raises
        ------
        TypeError
            if the parameter is not Pin()
        ValueError
            if the Pin is already included
        """
        if len(argv) > 0 and not isinstance(argv[0],Pin):
            raise TypeError('Inputs need to be Pin() objects')

        addIDsToDict(self.pins, *argv)

    def remove_pin(self,*argv):
        """The function to remove Pin objects from an Assembly which
        already has previously included pins.

        Parameters
        ----------
        *argv : Pin() or more Pin() objects
            Pin() objects to be added in the Assembly

        Examples
        --------
        >>> fuel=Pin('1')
        >>> guide=Pin('2')
        >>> assembly=Assembly(2,2)
        >>> assembly.set_pins(fuel,guide)
        >>> assembly.pins
        {'1': Pin(pinID=1), '2': Pin(pinID=2)}
        >>> assembly.remove_pin(guide)
        >>> assembly.pins
        {'1': Pin(pinID=1)}
        >>> assembly.remove_pin(guide)
        You can remove only existing Pin()

        Raises
        ------
        TypeError
            if the parameter is not Pin()
        ValueError
            if the Pin is already included
        TypeError
            if :attr:`pins` is None.
        """
        if len(argv) > 0 and not isinstance(argv[0],Pin):
            raise TypeError('Inputs need to be Pin() objects')

        delIDsFromDict(self._pins, *argv)

    def set_fuelmap(self,fuelmap=None):
        """The function to set the fuelmap of the Assembly

        Parameters
        ----------
        fuelmap : 2D array (NxM shape)
            fuelmap of the lattice

        Example
        -------
        >>> fuel=Pin('1')
        >>> fuel.add_region(uo2,0.5)
        >>> fuel.add_region(he,0.51)
        >>> fuel.add_region(zr,0.61)
        >>> fuelmap=[['1','1'],
                     ['1','1']]
        >>> assy=Assembly(2,2)
        >>> assy.set_fuelmap(fuelmap)
        """
        fuelmap=np.array(fuelmap)
        if  fuelmap.shape[0] != self.N or fuelmap.shape[1] != self.M:
            raise ValueError('Fuelmap has wrong size')
        else:
            self._fuelmap=fuelmap

    def set_coolant(self, coolant=None):
        """The function to set the coolant material in the Assembly

        Parameters
        ----------
        coolant : Material()
            the coolant material
        """
        if isinstance(coolant, Material):
            self._coolant=coolant._id
        else:
            raise TypeError('Material() is expected')

    def set_surrounding(self, surrounding=None):
        """The function to set the surrounding material around the Assembly

        Parameters
        ----------
        surrounding : Material()
            the surrounding material
        """
        if isinstance(surrounding, Material):
            self._surrounding=surrounding._id
        else:
            raise TypeError('Material() is expected')

    def set_source(self, *args):
        """The function to set the source material(s) in the Assembly

        Parameters
        ----------
        *args : Material() instances
            the source material(s)
        """
        self._source=[]
        for arg in args:
            if isinstance(arg,Material):
                self._source.append(arg._id)

    def set_pool(self,pool=None):
        """The function to set the pool around the Assembly

        Parameters
        ----------
        pool : Rectangle()
            the shape of the pool
        """
        if isinstance(pool,Rectangle):
            self._pool=pool
        else:
            raise TypeError('Pool has to be a Rectangle() object')

    def checkComplete(self):
        """
        The function to check whether everything is defined correctly in an
        Assembly() object. Prints messages indicating any problem.

            - checks whether any attribute is not defined (pool does not need
              to be defined)
            - checks whether any pin contains any region with radius greater
              than the pitch
            - checks whether all the pins in the fuelmap are attributed to
              the assembly
            - in case a pool is defined, it is checked whether the pool is
              around the assembly.

        Returns
        -------
        bool
            True if everything is correct and complete, False otherwise

        """
        if self.pins is None or self.pitch is None or \
           self.coolant is None or self.fuelmap is None or \
           self.source is None:
            print('ERROR: Assembly is not complete.')
            return False
        else:
            if False in [r<=self.pitch/2 for pin in self.pins.values() for r in pin._radii]:
                print('ERROR: in a Pin() a radius is greater than the pitch')
                return False

            if [] in [pin._radii for pin in self.pins.values()]:
                print('Warning: a pin has no regions, considered as coolant channel')

            if False in [self.fuelmap[i][j] in self.pins for i in range(self.N) for j in range(self.M)]:
                print('ERROR: Assembly().fuelmap contains pin not included in Assembly.Pins()')
                return False

            if self.pool is None:
                print('Warning: no pool in the problem, the surrounding of the Assembly is filled with coolant material')
                self._surrounding=self._coolant
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
                        if pooldummy.encloses_point(corner): #TODO use corners
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
    """A class used to represent a Detector.

    Parameters
    ----------
    detID : str
        ID of the detector

    Attributes
    ----------
    detID : str
        ID of the detector
    location : Point()
        location of the detector
    collimator : Collimator(), optional
        Collimator placed between the source and the detector
    """

    _idName = 'detID'

    def __init__(self, *args, **kwargs):
        self._location=None
        self._collimator=None
        self._id = getID(self._idName, args, kwargs)

    def __repr__(self):
        return "Detector(detID=%s)" % (self._id)

    @property
    def location(self):
        return self._location

    @property
    def collimator(self):
        return self._collimator

    def set_location(self,location=None):
        """The function to set the location of Detector

        Parameters
        ----------
        location : Point()
            location of the Detector
        """
        if isinstance(location,Point):
            self._location=location
        else:
            raise TypeError('Detector location has to be Point() object')

    def set_collimator(self,collimator=None):
        """The function to set the Collimator of Detector

        Parameters
        ----------
        collimator : Collimator()
            Collimator between source and Detector
        """
        if isinstance(collimator,Collimator):
            self._collimator=collimator
        else:
            raise TypeError('Collimator has to be Collimator() object')

class Absorber(object):
    """A class used to represent an Absorber.
    An absorber can be thought of any element around (or within) the assembly,
    which attenuates gamma radiation.

    Parameters
    ----------
    absID : str
        ID of the absorber

    Attributes
    ----------
    absID : str
        ID of the absorber
    form : Rectangle() or Circle()
        the shape of the absorber
    material : str
        matID of the Material the absorber is made of
    accommat : str
        matID of the Material the absorber is surrounded with (Note: the program
        has no capabilities to decide which material is around the absorber, thus
        the user has to set this)
    """

    _idName = 'absID'

    def __init__(self, *args, **kwargs):
        self._form=None
        self._material=None
        self._accommat=None
        self._id = getID(self._idName, args, kwargs)

    def __repr__(self):
        return "Absorber(absID=%s)" % (self._id)

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
        """The function to set the shape of Absorber

        Parameters
        ----------
        form : Rectangle() or Circle()
            shape of the absorber
        """
        if isinstance(form,Rectangle) or isinstance(form,Circle):
            self._form=form
        else:
            raise TypeError('Absorber has to be a Rectangle or Circle object')

    def set_material(self, material=None):
        """The function to set the material of Absorber

        Parameters
        ----------
        material : Material()
            Material the Absorber is made of
        """
        if isinstance(material, Material):
            self._material=material._id
        else:
            raise TypeError('Material() is expected')

    def set_accommat(self, accommat=None):
        """The function to set the accommodating material of Absorber

        Parameters
        ----------
        accommat : Material()
          Material the Absorber is surrounded with.
        """
        if isinstance(accommat, Material):
            self._accommat=accommat._id
        else:
            raise TypeError('Material() is expected')

class Collimator(object):
    """A class used to represent a Collimator.
    Any gamma ray not passing through the Collimator will be rejected. Collimators
    have an impact only if they are attributed to Detector objects with
    :meth:`Detector.set_collimator()`.
    The front and the back of the collimator cannot intersect.

    Parameters
    ----------
    collID : str (optional)
      ID of the collimator

    Attributes
    ----------
    collID : str (optional)
      ID of the collimator
    front : Segment()
      First ppening of the collimator slit
    back : Segment()
      Second opening of the collimator slit
    color : str
      color of the collimator in case of plotting the geometry.
    """

    idName = 'collID'

    def __init__(self, *args, **kwargs):
        self._front=None
        self._back=None
        self._color=None
        self._id = getID(self.idName, args, kwargs)

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
        """The function to set the front of the Collimator.
        Intersecting front and back is not accepted.

        Parameters
        ----------
        front : Segment()
          Opening of the collimator slit

        Examples
        ----------
        >>> c1=Collimator()
        >>> c1.set_back(Segment(Point(0,0),Point(1,0)))
        >>> c1.set_front(Segment(Point(0.5,-1),Point(0.5,1)))
        ValueError('Collimator back and front should not intersect')
        """
        if isinstance(front,Segment):
            if self._back is None:
                self._front=front
            elif len(self._back.intersection(front))>0:
                return ValueError('Collimator back and front should not intersect')
            else:
                self._front=front
        else:
            raise TypeError('Collimator front has to be a Segment object')

    def set_back(self,back=None):
        """The function to set the back of the Collimator.
        Intersecting front and back is not accepted.

        Parameters
        ----------
        back : Segment()
          Opening of the collimator slit
        """
        if isinstance(back,Segment):
            if self._front is None:
                self._back=back
            elif len(self._front.intersection(back))>0:
                return ValueError('Collimator back and front should not intersect')
            else:
                self._back=back

        else:
            raise TypeError('Collimator back has to be a Segment object')

    def set_color(self, color=None):
        """The function to set the color of the Collimator in case of plotting.

        Parameters
        ----------
        color : str
          color definition of Collimator in hex format.
        """
        if type(color) is str and is_hex_color(color):
            self._color=color
        else:
            raise ValueError(('Color has to be hex str for Material ID="{}"'.format(self._id)))

class Experiment(object):
    """A class used to represent an Experiment. An experiment is a complete passive
    gamma spectroscopy measurment setup with an assembly and detectors (absorbers
    and collimators are optional).

    Attributes
    ----------
    assembly : Assembly()
        The Assembly containing the source
    pins : dict
        Dictionary containing the available pin types.
    materials : dict
        Dictionary containing the available materials
    detectors : dict
        Dictionary containing the detectors in the problem
    absorbers : dict, optional
        Dictionary containing the absorbers in the problem
    elines : list of float, optional
        Energy lines (in MeV) at which the geometric efficiency is computed (in case missing,
        only the distance travelled in various material is computed)
    mu : dict
        The total attenuation coefficients for all the energies in elines, and for
        each material in the problem.
    sourcePoints : list
        List of pin-wise source point locations for each random sample.
    dTmap : dict of dictionaries of 2D numpy arrays
        The average distance travelled by a gamma-ray from a lattice position to a detector
        given for each material in the problem. Outer keys are :attr:`Detector._id` identifiers,
        inner keys are :attr:`Material._id` identifiers. It is an average of all
        random samples (which are kept track in :attr:`Experiment.dTmaps`)
    dTmapErr : dict of dictionaries of 2D numpy arrays
        The standard deviation of distance travelled by a gamma-ray from a lattice position to a detector
        given for each material in the problem. Outer keys are :attr:`Detector._id` identifiers,
        inner keys are :attr:`Material._id` identifiers. It is an standard deviation of all
        random samples (which are kept track in :attr:`Experiment.dTmaps`)
    dTmaps : list of dictionaries of 2D numpy arrays
        All random samples of distance travelled by a gamma-ray from a lattice position
        to a detector. Source point for each sample are stored in :attr:`Experiment.sourcePoints`
    contributionMap : dict
        Dictionary to store the rod-wise contributions averaged over random samples
        to each detector at each energy.
        Outer keys are detector :attr:`Detector.detID` identifiers.
        Inner keys are energy lines (as given in :meth:`Experiment.set_elines()`)
        contributionMap[detID][eline] is an NxM shaped numpy array, where
        N is :attr:`Assembly.N` and M is :attr:`Assembly.M`
    contributionMapErr : dict
        Dictionary to store the standard deviation of rod-wise contributions averaged over
        random samples to each detector at each energy.
        Outer keys are detector :attr:`Detector.detID` identifiers.
        Inner keys are energy lines (as given in :meth:`Experiment.set_elines()`)
        contributionMapErr[detID][eline] is an NxM shaped numpy array, where
        N is :attr:`Assembly.N` and M is :attr:`Assembly.M`
    contributionMaps : list
        All random samples of contribution maps to each detector at each energy.
    contributionMapAve : dict
        Dictionary to store the rod-wise contribution averaged over all detectors at each energy
        averaged over all random samples.
        Keys are energy lines (as given in :meth:`Experiment.set_elines()`)
        contributionMapAve[eline] is an NxM shaped numpy array, where
        N is :attr:`Assembly.N` and M is :attr:`Assembly.M`
    contributionMapAveErr : dict
        Dictionary to store the standard deviation of the pin-wise contribution averaged over
        all detectors at each energy averaged over all random samples.
        Keys are energy lines (as given in :meth:`Experiment.set_elines()`)
        contributionMapAveErr[eline] is an NxM shaped numpy array, where
        N is :attr:`Assembly.N` and M is :attr:`Assembly.M`
    contributionMapAves : list
        All random samples of the pin-wise contribution averaged over
        all detectors at each energy.
    geomEff : dict
        Dictionary to store the geometric efficiency at each detector location averaged over
        each random sample.
        Keys are detector :attr:`Detector._id` identifiers.
        geomEff[detID] is E long numpy array, where E is the length of :attr:`Experiment.elines`
    geomEffErr : dict
        Dictionary to store the standard deviation of the geometric efficiency 
        at each detector location averaged over each random sample.
        Keys are detector :attr:`Detector._id` identifiers.
        geomEff[detID] is E long numpy array, where E is the length of :attr:`Experiment.elines`
    geomEffs : list
        All random samples of the geometric efficiency at each detector location.
    geomEffAve : numpy.ndarray
        Geometric efficiency of the Experiment averaged over all detectors averaged over each
        random sample.
        The length is of :attr:`Experiment.elines`
    geomEffAveErr : numpy.ndarray
        Standard deviation of the geometric efficiency of the Experiment averaged over all 
        detectors averaged over each random sample.
        The length is of :attr:`Experiment.elines`
    geomEffAves : list
        All random samples of the geometric efficiency of the Experiment averaged over all 
        detectors.
    output : str, optional
      filename (and path) where to print the geometric efficiency

    Examples
    --------
    Examples of plotting attributes can be found at https://github.com/ezsolti/feign/blob/master/examples/ex1_2x2fuel.ipynb

    """
    def __init__(self):
        self._output=None
        self._assembly=None
        self._pins=None
        self._materials=None
        self._detectors=None
        self._absorbers=None
        self._elines=None
        self._mu=None
        self._sourcePoints=None
        self._dTmap=None
        self._dTmapErr=None
        self._dTmaps=None
        self._contributionMap=None
        self._contributionMapErr=None
        self._contributionMaps=None
        self._contributionMapAve=None
        self._contributionMapAveErr=None
        self._contributionMapAves=None
        self._geomEff=None
        self._geomEffErr=None
        self._geomEffs=None
        self._geomEffAve=None
        self._geomEffAveErr=None
        self._geomEffAves=None
        self._randomNum=1

    def __repr__(self):
        return "Experiment()"

    @property
    def output(self):
        return self._output

    @property
    def assembly(self):
        return self._assembly

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
    def dTmapErr(self):
        return self._dTmapErr

    @property
    def dTmaps(self):
        return self._dTmaps

    @property
    def contributionMap(self):
        return self._contributionMap

    @property
    def contributionMapErr(self):
        return self._contributionMapErr
    
    @property
    def contributionMaps(self):
        return self._contributionMaps

    @property
    def contributionMapAve(self):
        return self._contributionMapAve

    @property
    def contributionMapAveErr(self):
        return self._contributionMapAveErr

    @property
    def contributionMapAves(self):
        return self._contributionMapAves
    
    @property
    def mu(self):
        return self._mu

    @property
    def geomEff(self):
        return self._geomEff

    @property
    def geomEffErr(self):
        return self._geomEffErr

    @property
    def geomEffs(self):
        return self._geomEffs
    
    @property
    def geomEffAve(self):
        return self._geomEffAve
    
    @property
    def geomEffAveErr(self):
        return self._geomEffAveErr
    
    @property
    def geomEffAves(self):
        return self._geomEffAves

    @property
    def randomNum(self):
        return self._randomNum

    def set_random(self,randomNum=1):
        """The function to set number of random source locations per pin.

        Parameters
        ----------
        randomNum : int
          number of random source locations in each pin.
        """
        if isinstance(randomNum, int):
            self._randomNum=randomNum
        else:
            raise TypeError('Has to be int')

    def set_output(self,output='output.dat'):
        """The function to set the output file for printing the geometric efficiency

        Parameters
        ----------
        output : str
          filename and path where to print the geometric efficiency.
        """
        if isinstance(output, str):
            self._output=output
        else:
            raise TypeError('Output filename has to be str')

    def set_materials(self,*argv):
        """The function to include Material objects in an Experiment

        Parameters
        ----------
        *argv : Material() or more Material() objects
            Material() objects to be included in the Experiment

        Examples
        --------
        >>> uox=Material('1')
        >>> zr=Material('2')
        >>> experiment=Experiment()
        >>> experiment.materials

        >>> experiment.set_materials(uox,zr)
        >>> experiment.materials
        {'1': Material(matID=1), '2': Material(matID=2)}

        Raises
        ------
        TypeError
            if the parameter is not Material()
        ValueError
            if the Material is already included
        """
        self._materials={}
        self.add_material(*argv)

    def add_material(self,*argv):
        """The function to add Material objects to an Experiment, which may have
        already included materials. If one wants to rewrite the existing materials,
        then the :meth:`Experiment.set_materials()` has to be called.

        Parameters
        ----------
        *argv : Material() or more Material() objects
            Material() objects to be added in the Experiment

        Examples
        --------
        >>> uox=Material('1')
        >>> zr=Material('2')
        >>> experiment=Experiment()
        >>> experiment.set_materials()
        >>> experiment.materials
        {}
        >>> experiment.add_material(uox)
        >>> experiment.add_material(zr)
        >>> experiment.materials
        {'1': Material(matID=1), '2': Material(matID=2)}

        Raises
        ------
        TypeError
            if the parameter is not Material()
        ValueError
            if the Material is already included
        """
        if len(argv) > 0 and not isinstance(argv[0],Material):
            raise TypeError('Inputs need to be Material() objects')

        addIDsToDict(self._materials, *argv)

    def remove_material(self,*argv):
        """The function to remove Material objects from an Experiment which
        already has previously included materials.

        Parameters
        ----------
        *argv : Material() or more Material() objects
            Material() objects to be added in the Experiment

        Examples
        --------
        >>> uox=Material('1')
        >>> zr=Material('2')
        >>> experiment=Experiment()
        >>> experiment.set_materials(uox,zr)
        >>> experiment.materials
        {'1': Material(matID=1), '2': Material(matID=2)}
        >>> experiment.remove_material(zr)
        >>> experiment.materials
        {'1': Material(matID=1)}
        >>> experiment.remove_material(zr)
        You can remove only existing Material()

        Raises
        ------
        TypeError
            if the parameter is not Material()
        TypeError
            if :attr:`materials` is None.
        """
        if len(argv) > 0 and not isinstance(argv[0],Material):
            raise TypeError('Inputs need to be Material() objects')

        delIDsFromDict(self._materials, *argv)

    def set_absorbers(self,*argv):
        """The function to include Absorber objects in an Experiment

        Parameters
        ----------
        *argv : Absorber() or more Absorber() objects
            Absorber() objects to be included in the Experiment

        Examples
        --------
        >>> leadsheet=Absorber('leadsheet')
        >>> alusheet=Absorber('alusheet')
        >>> experiment=Experiment()
        >>> experiment.absorbers

        >>> experiment.set_absorbers(leadsheet,alusheet)
        >>> experiment.absorbers
        {'leadsheet': Absorber(absID=leadsheet), 'alusheet': Absorber(absID=alusheet)}

        Raises
        ------
        TypeError
            if the parameter is not Absorber()
        ValueError
            if the Absorber is already included
        """
        self._absorbers={}
        self.add_absorber(*argv)

    def add_absorber(self,*argv):
        """The function to add Absorber objects to an Experiment, which may have
        already included absorbers. If one wants to rewrite the existing absorbers,
        then the :meth:`Experiment.set_absorbers()` has to be called.

        Parameters
        ----------
        *argv : Absorber() or more Absorber() objects
            Absorber() objects to be added in the Experiment

        Examples
        --------
        >>> leadsheet=Absorber('leadsheet')
        >>> alusheet=Absorber('alusheet')
        >>> experiment=Experiment()
        >>> experiment.set_absorbers()
        >>> experiment.absorbers
        {}
        >>> experiment.add_absorber(leadsheet)
        >>> experiment.add_absorber(alusheet)
        >>> experiment.absorbers
        {'leadsheet': Absorber(absID=leadsheet), 'alusheet': Absorber(absID=alusheet)}

        Raises
        ------
        TypeError
            if the parameter is not Absorber()
        ValueError
            if the Absorber is already included
        """
        if len(argv) > 0 and not isinstance(argv[0],Absorber):
            raise TypeError('Inputs need to be Absorber() objects')

        addIDsToDict(self._absorbers, *argv)

    def remove_absorber(self,*argv):
        """The function to remove Absorber objects from an Experiment which
        already has previously included absorbers.

        Parameters
        ----------
        *argv : Absorber() or more Absorber() objects
            Absorber() objects to be added in the Experiment

        Examples
        --------
        >>> leadsheet=Absorber('leadsheet')
        >>> alusheet=Absorber('alusheet')
        >>> experiment=Experiment()
        >>> experiment.set_absorbers(leadsheet,alusheet)
        >>> experiment.absorbers
        {'leadsheet': Absorber(absID=leadsheet), 'alusheet': Absorber(absID=alusheet)}
        >>> experiment.remove_absorber(alusheet)
        >>> experiment.absorbers
        {'leadsheet': Absorber(absID=leadsheet)}
        >>> experiment.remove_absorber(alusheet)
        You can remove only existing Absorber()

        Raises
        ------
        TypeError
            if the parameter is not Absorber()
        TypeError
            if :attr:`absorbers` is None.
        """
        if len(argv) > 0 and not isinstance(argv[0],Absorber):
            raise TypeError('Inputs need to be Absorber() objects')

        delIDsFromDict(self._absorbers, *argv)

    def set_detectors(self,*argv):
        """The function to include Detector objects in an Experiment

        Parameters
        ----------
        *argv : Detector() or more Detector() objects
            Detector() objects to be included in the Experiment

        Examples
        --------
        >>> F5=Detector('F5')
        >>> F15=Detector('F15')
        >>> experiment=Experiment()
        >>> experiment.detectors

        >>> experiment.set_detectors(F5,F15)
        >>> experiment.detectors
        {'F5': Detector(detID=F5), 'F15': Detector(detID=F15)}

        Raises
        ------
        TypeError
            if the parameter is not Detector()
        ValueError
            if the Detector is already included
        """
        self._detectors={}
        self.add_detector(*argv)

    def add_detector(self,*argv):
        """The function to add Detector objects to an Experiment, which may have
        already included detectors. If one wants to rewrite the existing detectors,
        then the :meth:`Experiment.set_detectors()` has to be called.

        Parameters
        ----------
        *argv : Detector() or more Detector() objects
            Detector() objects to be added in the Experiment

        Examples
        --------
        >>> F5=Detector('F5')
        >>> F15=Detector('F15')
        >>> experiment=Experiment()
        >>> experiment.set_detectors()
        >>> experiment.detectors
        {}
        >>> experiment.add_detector(F5)
        >>> experiment.add_detector(F15)
        >>> experiment.detectors
        {'F5': Detector(detID=F5), 'F15': Detector(detID=F15)}

        Raises
        ------
        TypeError
            if the parameter is not Detector()
        ValueError
            if the Detector is already included
        """
        if len(argv) > 0 and not isinstance(argv[0],Detector):
            raise TypeError('Inputs need to be Detector() objects')

        addIDsToDict(self._detectors, *argv)

    def remove_detector(self,*argv):
        """The function to remove Detector objects from an Experiment which
        already has previously included detectors.

        Parameters
        ----------
        *argv : Detector() or more Detector() objects
            Detector() objects to be added in the Experiment

        Examples
        --------
        >>> F5=Detector('F5')
        >>> F15=Detector('F15')
        >>> experiment=Experiment()
        >>> experiment.set_detectors(F5,F15)
        >>> experiment.detectors
        {'F5': Detector(detID=F5), 'F15': Detector(detID=F15)}
        >>> experiment.remove_detector(F15)
        >>> experiment.detectors
        {'F5': Detector(detID=F5)}
        >>> experiment.remove_detector(F15)
        You can remove only existing Detector()

        Raises
        ------
        TypeError
            if the parameter is not Detector()
        TypeError
            if :attr:`detectors` is None.
        """
        if len(argv) > 0 and not isinstance(argv[0],Detector):
            raise TypeError('Inputs need to be Detector() objects')

        delIDsFromDict(self._detectors, *argv)

    def set_assembly(self,assembly=None):
        """The function to include Assembly in an Experiment

        Parameters
        ----------
        assembly : Assembly()
            Assembly to be included in Experiment
        """

        if isinstance(assembly,Assembly):
            self._assembly=assembly
            self._pins=self._assembly.pins
        else:
            raise ValueError('Assembly has to be an Assembly() object')

    def set_elines(self,elines=None):
        """The function to set energy lines at which the geometric efficiency is
        calculated

        Parameters
        ----------
        elines : list of str
            Energy lines (in MeV) at which the geometric efficiency is calculated.

        Note
        ----
        values of elines are strings, because they will be keys of :attr:`mu`
        """
        if isinstance(elines, list) and (False not in [isinstance(e, str) for e in elines]) and (False not in [isFloat(e) for e in elines]):
            self._elines=elines
        else:
            raise ValueError('elines has to be a list of str MeV values')

    def get_MuTable(self):
        """The function to create a nested dictionary to store the total
        attenuation coefficients.

        Returns
        -------
        dict
            Dictionary to store the attenuation coefficients.
            Outer keys are energies as defined in :attr:`elines`,
            inner keys are :attr:`Material.matID` identifiers.
        """
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
        """The function to calculate the distanced travelled in any material
        by a gamma ray emitted from any pin positions of the Assembly to a detector

        Parameters
        ----------
        detector : Detector()
        
        Returns
        -------
        dTmap : dict
            The travelled distance in various materials. Keys are material identifiers,
            values are pin-wise distance values.
        sourcePoint : numpy array
            Pin-wise source location in the given calculation. 
        """
        dTmap={key: np.zeros((self.assembly.N,self.assembly.M)) for key in self.materials}
        #sourcePoint=np.array([[0 for i in range(self.assembly.N)] for j in range(self.assembly.M)])
        sourcePoint=np.empty((self.assembly.N,self.assembly.M),dtype=object)
        #create distance seen maps for each material
        p=self.assembly.pitch/2
        N=self.assembly.N
        M=self.assembly.M
        for i in range(N):
            for j in range(M):
                sourceIn=[s in self.pins[self.assembly.fuelmap[i][j]]._materials for s in self.assembly.source]
                if True in sourceIn:                     

                    dT={key: 0 for key in self.materials} #dict to track distances travelled in each material for a given pin
                    
                    #TODO get a random number is the source material?!
                    #if source is the inner most pin randomly center in circle
                    #else: randomly in that and reject the things within
                    if self.randomNum == 1:
                        centerSource=Point(-p*(N-1)+j*2*p,p*(N-1)-i*2*p)
                    else:
                        length = self.pins[self.assembly.fuelmap[i][j]]._radii[0]*np.sqrt(np.random.uniform(0, 1)) #TODO, if second ring is the source?
                        angle = np.pi * np.random.uniform(0, 2)
                        xnoise = length * np.cos(angle)
                        ynoise = length * np.sin(angle)
                        centerSource=Point(-p*(N-1)+j*2*p,p*(N-1)-i*2*p).translate(xnoise,ynoise)                    
                    sourcePoint[i][j]=centerSource
                    segmentSourceDetector=Segment(centerSource,detector.location)
                    #Only track rays which pass through the collimator
                    if detector.collimator is None or (len(detector.collimator.front.intersection(segmentSourceDetector))==1 and
                       len(detector.collimator.back.intersection(segmentSourceDetector))==1):
                        
                       ###Distances traveled in other pin positions
                        for ii in range(N):
                            for jj in range(M):
                                centerShield=Point(-p*(N-1)+jj*2*p,p*(N-1)-ii*2*p)
                                pinChannel=Rectangle(centerShield.translate(-p,p),centerShield.translate(p,p),
                                                   centerShield.translate(p,-p),centerShield.translate(-p,-p))
#                                    print('------')
#                                    print(pinChannel)
#                                    print(segmentSourceDetector)
#                                    print('------')
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
                            elif len(intersects)==1: #if the detector or source is within absorber.
                                if absorber.form.encloses_point(detector.location):
                                    dabs=Point.distance(intersects[0],detector.location)
                                elif absorber.form.encloses_point(centerSource):
                                    dabs=Point.distance(intersects[0],centerSource)
                                    print('Warning: absorber #%s is around source at %.2f,%.2f'%(absorber._id,centerSource.x,centerSource.y))
                                else:
                                    raise ValueError('Ray has only one intersection with Absorber \n and the detector neither the source is enclosed by it.')
                            else: 
                                dabs=0
                            dT[absorber.material]=dT[absorber.material]+dabs
                            dT[absorber.accommat]=dT[absorber.accommat]-dabs
                        #Update the map
                        for key in dT:
                            dTmap[key][i][j]=dT[key]
                    else: #not through collimator
                        for key in dT:  
                            dTmap[key][i][j]=np.Inf
        
        return dTmap, sourcePoint

    def attenuation(self,dTmap,mue,detector,sourcePoint):
        """The function to calculate the pin-wise contribution to the detector
        at a given energy. That is the probablity that a gamma-ray emitted from 
        a pin will reach the detector point.

        Parameters
        ----------
        dTmap : dict
            The travelled distance in various materials. Keys are material identifiers,
            values are pin-wise distance values. Shape as created by :meth:`Experiment.distanceTravelled()`
        mue : dict
            Total attenuation coefficients at the given energy. Keys are materials,
            values are the total attenuation coefficient values. 
        detector : Detector()
        sourcePoint : numpy array
            Pin-wise source locations, as created by :meth:`Experiment.distanceTravelled()`.
        
        Returns
        -------
        contribmap : numpy array
            Pin-wise probabilities that a gamma-ray emitted from a given pin hits the detector.
        """
        p=self.assembly.pitch/2
        N=self.assembly.N
        M=self.assembly.M
        contribmap=np.zeros((N,M))
        for i in range(N):
            for j in range(M):
                center=sourcePoint[i][j]
                sourceIn=[s in self.pins[self.assembly.fuelmap[i][j]]._materials for s in self.assembly.source]
                if True in sourceIn:
                    contrib=1 #TODO might be a place to include a pre-known emission weight map. Or to provide a function which multiplies the contribution with some weight matrix
                    for key in self.materials.keys():
                        contrib=contrib*math.exp(-1*mue[key]*dTmap[key][i][j])
                    contribmap[i][j]=contrib/(4*math.pi*(Point.distance(center,detector.location))**2)
        return contribmap

    def checkComplete(self):
        """Function to check whether everything is defined correctly in an
           Experiment() object.

           - checks whether assembly is complete
           - checks whether any pin contains any region with radius greater than the pitch
           - checks whether all the pins in the fuelmap are attributed to the assembly
           - in case a pool is defined, it is checked whether the pool is around the assembly.

           Returns
           ----------
           bool
             True if everything is correct and complete, False otherwise
        """

        errors=[]
        if self.materials is None:
            print('ERROR: Materials are not defined')
            return False #otherwise the following checks cannot be done.

        if self.assembly is None:
            print('ERROR: Assembly is missing')
            errors.append(False)
        else:
            if not self.assembly.checkComplete():
                errors.append(False)
            else:
                if False in [mat in self.materials for pin in self.pins.values() for mat in pin._materials]:
                    print('ERROR: pin material is missing from materials')
                    errors.append(False)

                if False in [source in self.materials for source in self.assembly.source]:
                    print('ERROR: source material is not in Materials')
                    errors.append(False)


        if self.detectors is None:
            print('ERROR: no detector is defined.')
            errors.append(False)
        else:
            if True in [det.location is None for det in self.detectors.values()]:
                print('ERROR: Detector location is not defined')
                errors.append(False)
            if True in [det.collimator.back is None or det.collimator.front is None for det in self.detectors.values() if det.collimator is not None]:
                print('ERROR: One collimator is not fully defined')
                errors.append(False)

        if self.absorbers is None:
            self.set_absorbers()
            print('No absorbers in the problem')
        else:
            if self.absorbers is not None and False in [absorber.material in self.materials for absorber in self.absorbers.values()]:
                print('ERROR: absorber material is missing from materials')
                errors.append(False)
            if self.absorbers is not None and False in [absorber.accommat in self.materials for absorber in self.absorbers.values()]:
                print('ERROR: Absorber accommodating material is missing from materials')
                errors.append(False)
        if self._elines is None:
            print('Warning: elines missing; only distance travelled in various materials will be computed')
        else:
            if True in [mat.density is None for mat in self.materials.values()]:
                print('ERROR: Material density is missing')
                errors.append(False)
            if True in [mat.path is None for mat in self.materials.values()]:
                print('ERROR: Path for attenuation file missing')
                errors.append(False)

        if len(errors)==0:
            return True
        else:
            print('%d errors encountered.'%(len(errors)))
            return False

    def Plot(self,out=None,dpi=600,xl=[-100,100],yl=[-100,100],detectorSize=0.4):
        """Function to plot the geometry of an Experiment() object.
           The function will randomly set colors to Material() objects for which colors
           were previously not defined.

           Parameters
           ----------
           out : str (default=None)
             name of output file
           dpi : int (default=600)
             dpi of the saved plot
           xl : list of float (default=[-100,100])
             x-direction limits of region of the geometry to plot (in cm)
           yl : list of float (default=[-100,100])
             y-direction limits of region of the geometry to plot (in cm)
           detectorSize : float (default=400)
             radius of white circle to illustrate the detector points
        """
        if self.checkComplete() is False:
            raise ValueError('ERROR')

        import random
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
        """The function to run an Experiment. It will update the dTmap, the
        contributionMap and the geomEff attributes.
        """
        if self.checkComplete() is False:
            raise ValueError('ERROR')
        
        sourceNorm=0
        for i in range(self.assembly.N):
            for j in range(self.assembly.M):
                sourceIn=[s in self.pins[self.assembly.fuelmap[i][j]]._materials for s in self.assembly.source]
                if True in sourceIn:
                    sourceNorm=sourceNorm+1
        dTmaps=[]
        contributionMaps=[]
        contributionMapAves=[]
        geomefficiencies=[]
        geomefficiencyAves=[]
        sourcePoints=[]
        for k in range(self.randomNum):
            print('#%d is being calculated'%(k)) #TODO RUN-ba
            dTmap={}
            for name in self.detectors:
                print("Distance travelled to detector "+name+" is being calculated")
                dTmap[name],sourcePoint=self.distanceTravelled(self.detectors[name]) 
            dTmaps.append(dTmap)
            sourcePoints.append(sourcePoint)    
            if self._elines is not None:
                if k==0:
                    self.get_MuTable()
                geomefficiency={}
                geomefficiencyAve=np.zeros(len(self._elines))
                contributionMapAve={e: np.zeros((self.assembly.N,self.assembly.M)) for e in self._elines}
                contributionMap={}
                for name in self.detectors:
                    print('Contribution to detector %s is calculated...'%(name))
                    contributionMap[name]={}
                    geomefficiency[name]=np.zeros(len(self._elines))
                    for e in self._elines:
                        print('...for gamma energy %s MeV'%(e))
                        mue=self._mu[e]
                        muem={key: mue[key]*self.materials[key].density for key in mue.keys()}
                        contributionMap[name][e]=self.attenuation(dTmap[name],muem,self.detectors[name],sourcePoint)
                        contributionMapAve[e]=contributionMapAve[e]+contributionMap[name][e]/len(self.detectors)
                    geomefficiency[name]=np.array([np.sum(contribution) for contribution in contributionMap[name].values()])/sourceNorm
                    geomefficiencyAve=geomefficiencyAve+geomefficiency[name]/len(self.detectors)
                contributionMaps.append(contributionMap)
                contributionMapAves.append(contributionMapAve)
                geomefficiencies.append(geomefficiency)
                geomefficiencyAves.append(geomefficiencyAve)            
        self._sourcePoints=sourcePoints
        #Various Numpy manipulations to restructure the "plural" lists containing data for
        #each random sample. Then the mean and the std of the "plural" lists is calculated.
        
        #restructuring dTmaps: from the list of dictionaries, make a dictionary of lists
        #then take the mean and std of the maps in the inner list
        dTmapsRe={det: {mat: [dmap[det][mat] for dmap in dTmaps] for mat in self.materials} for det in self.detectors}
        dTmap={} #will be the average
        dTmapErr={} #will be the std
        for det in dTmapsRe:
            dTmap[det]={}
            dTmapErr[det]={}
            for mat in dTmapsRe[det]:
                dTmapToAve=np.array([np.ravel(dT) for dT in dTmapsRe[det][mat]])
                dTmap[det][mat]=np.mean(dTmapToAve,axis=0).reshape((self.assembly.N,self.assembly.M))
                dTmapErr[det][mat]=np.std(dTmapToAve,axis=0).reshape((self.assembly.N,self.assembly.M))
        self._dTmap=dTmap
        self._dTmapErr=dTmapErr
        self._dTmaps=dTmaps
         
        if self._elines is not None:  
            #restructuring contributionMaps
            contributionMapsRe={det: {e: [cmap[det][e] for cmap in contributionMaps] for e in self._elines} for det in self.detectors}
            contributionMap={} #will be the average
            contributionMapErr={} #will be the stdcontributionMapAves
            for det in contributionMapsRe:
                contributionMap[det]={}
                contributionMapErr[det]={}
                for e in contributionMapsRe[det]:
                    cMapToAve=np.array([np.ravel(cm) for cm in contributionMapsRe[det][e]])
                    contributionMap[det][e]=np.mean(cMapToAve,axis=0).reshape((self.assembly.N,self.assembly.M))
                    contributionMapErr[det][e]=np.std(cMapToAve,axis=0).reshape((self.assembly.N,self.assembly.M))
            self._contributionMap=contributionMap
            self._contributionMapErr=contributionMapErr
            self._contributionMaps=contributionMaps
            
            #restructuring contributionMapAves
            contributionMapAvesRe={e: [cmap[e] for cmap in contributionMapAves] for e in self._elines}
            contributionMapAve={} #will be the average
            contributionMapAveErr={} #will be the std
            for e in contributionMapAvesRe:
                cMapToAve=np.array([np.ravel(cm) for cm in contributionMapAvesRe[e]])
                contributionMapAve[e]=np.mean(cMapToAve,axis=0).reshape((self.assembly.N,self.assembly.M))
                contributionMapAveErr[e]=np.std(cMapToAve,axis=0).reshape((self.assembly.N,self.assembly.M))
            self._contributionMapAve=contributionMapAve
            self._contributionMapAveErr=contributionMapAveErr
            self._contributionMapAves=contributionMapAves
   
            #restructuring geomefficiencies
            geomefficienciesRe={det: [geff[det] for geff in geomefficiencies] for det in self._detectors}
            geomefficiency={} #will be the average
            geomefficiencyErr={} #will be the std
            for det in geomefficienciesRe:
                geffToAve=np.array([geff for geff in geomefficienciesRe[det]])
                geomefficiency[det]=np.mean(geffToAve,axis=0)
                geomefficiencyErr[det]=np.std(geffToAve,axis=0)
            self._geomEff=geomefficiency
            self._geomEffErr=geomefficiencyErr
            self._geomEffs=geomefficiencies
            
            #restructuring geomefficiencyAves
            geomefficiencyAve=np.mean(np.array([geff for geff in geomefficiencyAves]),axis=0)
            geomefficiencyAveErr=np.std(np.array([geff for geff in geomefficiencyAves]),axis=0)
            self._geomEffAve=geomefficiencyAve
            self._geomEffAveErr=geomefficiencyAveErr
            self._geomEffAves=geomefficiencyAves
            
            if self.output is not None:
                output=open(self.output,'w')
                for e,c in zip(self._elines,self._geomEffAve):
                    output.write(e+'\t'+str(c)+'\n')
                output.close()