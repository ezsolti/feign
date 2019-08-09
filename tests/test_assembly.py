#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test Assembly() checkComplete() function
"""

import unittest
from feign.blocks import *

fuelmap= [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '3', '1', '1', '1', '1', '1', '1', '1', '1', '1', '3', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '3', '1', '1', '1', '1', '1', '1', '1', '1', '1', '3', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '3', '1', '1', '3', '1', '1', '3', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
          ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]

uo2=Material('1')
uo2.set_density(10.5)
uo2.set_path(('/dataFin/UO2.dat',1))

he=Material('2')
he.set_density(0.00561781)
he.set_path(('/dataFin/He.dat',1))

zr=Material('3')
zr.set_density(6.52)
zr.set_path(('/dataFin/Zr.dat',1))

h2o=Material('4')
h2o.set_density(1.0)
h2o.set_path(('/dataFin/H2O.dat',1))

ss=Material('5')
ss.set_density(8.02)
ss.set_path(('/dataFin/SS.dat',1))

air=Material('6')
air.set_density(0.001225)
air.set_path(('/dataFin/Air.dat',1))

fuel=Pin('1')
fuel.add_region(uo2,0.41)
fuel.add_region(he,0.42)
fuel.add_region(zr,0.48)


rodguide=Pin('3')
rodguide.add_region(h2o,0.42)
rodguide.add_region(zr,0.48)

class TestAssemblyCheckComplete(unittest.TestCase):
    def test1_pool_inside_fuel_assembly(self):
        assembly=Assembly(17,17)
        assembly.set_pitch(1.26)
        assembly.set_source(uo2)
        assembly.set_coolant(h2o)
        assembly.set_surrounding(air)
        assembly.set_pins(fuel, rodguide)
        assembly.set_fuelmap(fuelmap)
        pool=Rectangle(Point(5,5),Point(5,-5),Point(-5,-5),Point(-5,5))
        assembly.set_pool(pool)
        self.assertFalse(assembly.checkComplete())
    def test2_pool_cuts_fuel_assembly(self):
        assembly=Assembly(17,17)
        assembly.set_pitch(1.26)
        assembly.set_source(uo2)
        assembly.set_coolant(h2o)
        assembly.set_surrounding(air)
        assembly.set_pins(fuel, rodguide)
        assembly.set_fuelmap(fuelmap)
        pool=Rectangle(Point(15,0),Point(0,-15),Point(-15,0),Point(0,15)) #this will cut the assembly
        assembly.set_pool(pool)
        self.assertFalse(assembly.checkComplete())
    def test3_not_complete_assembly(self):
        assembly=Assembly(17,17)
        #assembly.set_pitch(1.26) Missing attribute!
        assembly.set_source(uo2)
        assembly.set_coolant(h2o)
        assembly.set_surrounding(air)
        assembly.set_pins(fuel, rodguide)
        assembly.set_fuelmap(fuelmap)
        pool=Rectangle(Point(77,0),Point(0,-77),Point(-77,0),Point(0,77))
        assembly.set_pool(pool)
        self.assertFalse(assembly.checkComplete())
    def test4_too_large_pin_in_assembly(self):
        assembly=Assembly(17,17)
        pintest=Pin('3')
        pintest.add_region(uo2,0.41)
        pintest.add_region(zr,0.7) #2*0.7>1.26
        assembly.set_pitch(1.26)
        assembly.set_source(uo2)
        assembly.set_coolant(h2o)
        assembly.set_surrounding(air)
        assembly.set_pins(fuel,pintest)
        assembly.set_fuelmap(fuelmap)
        pool=Rectangle(Point(77,0),Point(0,-77),Point(-77,0),Point(0,77))
        assembly.set_pool(pool)
        self.assertFalse(assembly.checkComplete())
    def test5_fuelmap_pin_not_in_assembly(self):
        assembly=Assembly(17,17)
        pintest=Pin('2')
        pintest.add_region(uo2,0.41)
        pintest.add_region(zr,0.45)
        assembly.set_pitch(1.26)
        assembly.set_source(uo2)
        assembly.set_coolant(h2o)
        assembly.set_surrounding(air)
        assembly.set_pins(fuel,pintest) #'1' and '2', while fuelmap wants '3' as well
        assembly.set_fuelmap(fuelmap)
        pool=Rectangle(Point(77,0),Point(0,-77),Point(-77,0),Point(0,77))
        assembly.set_pool(pool)
        self.assertFalse(assembly.checkComplete())
    def test6_OK_assembly(self):
        assembly=Assembly(17,17)
        assembly.set_pitch(1.26)
        assembly.set_source(uo2)
        assembly.set_coolant(h2o)
        assembly.set_surrounding(air)
        assembly.set_pins(fuel, rodguide)
        assembly.set_fuelmap(fuelmap)
        pool=Rectangle(Point(77,0),Point(0,-77),Point(-77,0),Point(0,77))
        assembly.set_pool(pool)
        self.assertTrue(assembly.checkComplete())

if __name__ == '__main__':
    unittest.main()
