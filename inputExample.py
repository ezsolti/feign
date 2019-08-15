#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PWR 17x17 input example, 2 detectors, one with absorber sheets

zs. elter 2019
"""

from feign.geometry import *
from feign.blocks import *

uo2=Material('1')
uo2.set_density(10.5)
uo2.set_path(('/data/UO2.dat',1))

he=Material('2')
he.set_density(0.00561781)
he.set_path(('/data/He.dat',1))

zr=Material('3')
zr.set_density(6.52)
zr.set_path(('/data/Zr.dat',1))

h2o=Material('4')
h2o.set_density(1.0)
h2o.set_path(('/data/H2O.dat',1))

ss=Material('5')
ss.set_density(8.02)
ss.set_path(('/data/SS.dat',1))

air=Material('6')
air.set_density(0.001225)
air.set_path(('/data/Air.dat',1))

lead=Material('7')
lead.set_density(11.34)
lead.set_path(('/data/Pb.dat',1))

copper=Material('8')
copper.set_density(8.96)
copper.set_path(('/data/Cu.dat',1))

alu=Material('9')
alu.set_density(2.7)
alu.set_path(('/data/Al.dat',1))

###Pins

fuel=Pin('1')
fuel.add_region(uo2,0.41)
fuel.add_region(he,0.42)
fuel.add_region(zr,0.48)

waterchannel=Pin('2')

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

F5alu3mm=Absorber('F5alu3mm')
F5alu3mm.set_form(Rectangle(Point(145.805, 202.374),Point(202.374, 145.805),
                                           Point(202.162, 145.593),Point(145.593, 202.162)))
F5alu3mm.set_material(alu)
F5alu3mm.set_accommat(air)

F5cooper1mm=Absorber('F5cooper1mm')
F5cooper1mm.set_form(Rectangle(Point(144.108, 200.677),Point(200.677, 144.108),
                                           Point(200.606, 144.0376),Point(144.0376, 200.606)))
F5cooper1mm.set_material(copper)
F5cooper1mm.set_accommat(air)

F5lead8mm=Absorber('F5lead8mm')
F5lead8mm.set_form(Rectangle(Point(146.37, 202.94),Point(202.94, 146.37),
                                           Point(202.374, 145.805),Point(145.805, 202.374)))
F5lead8mm.set_material(lead)
F5lead8mm.set_accommat(air)

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
 

pwrClab=Experiment()
pwrClab.set_assembly(pwrOrig)
pwrClab.set_elines(elines)
pwrClab.set_output('outputExample.dat')
pwrClab.set_detectors(F5,F15)
pwrClab.set_absorbers(F5alu3mm,F5cooper1mm,F5lead8mm,F5steel21mm)
pwrClab.set_materials(uo2,he,zr,h2o,ss,air,lead,copper,alu)
pwrClab.Run()
