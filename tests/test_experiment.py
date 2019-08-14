#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test Experiment checkComplete()

zs. elter 2019

Note, at the beginning basically everything needs to be created, and in the test
functions only an Experiment() object will be manipulated.
"""


import unittest
from feign.blocks import *
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



###Pins

fuel=Pin('1')
fuel.add_region(uo2,0.41)
fuel.add_region(he,0.42)
fuel.add_region(zr,0.48)


rodguide=Pin('3')
rodguide.add_region(h2o,0.42)
rodguide.add_region(zr,0.48)

###Assembly

pwrOrig=Assembly(17,17)
pwrOrig.set_pitch(1.26)
pwrOrig.set_source(uo2)
pwrOrig.set_coolant(h2o)
pwrOrig.set_surrounding(air)
pwrOrig.set_pins(fuel,rodguide)

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

pwrOrig.set_fuelmap(fuelmap)
pool=Rectangle(Point(-77.78, 0.0),Point(0.0, 77.78),Point(77.78, 0.0),Point(0.0, -77.78))
pwrOrig.set_pool(pool)


F5=Detector('F5')
F5.set_location(Point(174.726, 174.726))
F15=Detector('F15')
F15.set_location(Point(-174.726, -174.726))

###collimators could come here



F5steel21mm=Absorber('F5steel21mm')
F5steel21mm.set_form(Rectangle(Point(145.593, 202.162),Point(202.162, 145.593),
                                           Point(200.677, 144.108),Point(144.108, 200.677)))
F5steel21mm.set_material(ss)
F5steel21mm.set_accommat(air)


                
elines=['0.4971',
 '0.563',
 '0.569',
 '0.6006',
 '0.604',
 '0.6103',
 '0.621',
 '0.635',
 '0.662',
 '0.723',
 '0.724',
 '0.756',
 '0.757',
 '0.765',
 '0.795',
 '0.801',
 '0.873',
 '0.996',
 '1.004',
 '1.038',
 '1.05',
 '1.167',
 '1.205',
 '1.246',
 '1.274',
 '1.365',
 '1.494',
 '1.562',
 '1.596',
 '1.766',
 '1.797',
 '1.988',
 '2.112',
 '2.185']
 

class TestExperimentCheckComplete(unittest.TestCase):
    def test_experiment_missing_assembly(self):
        pwrClab=Experiment()
        #pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,zr,h2o,ss,air)
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_missing_pin_material(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,ss,air) #zr missing
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_materials_missing(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        #pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_detectors_missing(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        #pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_detector_location_missing(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        F5b=Detector('F5b')
        pwrClab.set_detectors(F5b,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_detector_collimator_not_complete(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        F5b=Detector('F5b')
        F5b.set_location(Point(174.726, 174.726))
        coll=Collimator('1')
        coll.set_back(Segment(Point(125.0,-11.6),Point(125.0,11.6)).rotate(45))
        F5b.set_collimator(coll)
        pwrClab.set_detectors(F5b,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_absorbers_missing_not_a_problem(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        #pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertTrue(pwrClab.checkComplete())
    def test_experiment_absorbers_material_missing(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,zr,air)
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_elines_missing_not_a_problem(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        #pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertTrue(pwrClab.checkComplete())
    def test_experiment_elines_is_there_material_density_missing(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        uo2=Material('1')
        pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertFalse(pwrClab.checkComplete())
    def test_experiment_everything_defined(self):
        pwrClab=Experiment()
        pwrClab.set_assembly(pwrOrig)
        pwrClab.set_elines(elines)
        pwrClab.set_detectors(F5,F15)
        pwrClab.set_absorbers(F5steel21mm)
        pwrClab.set_materials(uo2,he,h2o,zr,ss,air)
        self.assertTrue(pwrClab.checkComplete())
        
if __name__ == '__main__':
    unittest.main()



