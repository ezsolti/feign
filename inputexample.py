#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PWR 17x17 input example with absorber sheets
"""

from feign.geometry import *
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

lead=Material('7')
lead.set_density(11.34)
lead.set_path(('/dataFin/Pb.dat',1))

copper=Material('8')
copper.set_density(8.96)
copper.set_path(('/dataFin/Cu.dat',1))

alu=Material('9')
alu.set_density(2.7)
alu.set_path(('/dataFin/Al.dat',1))

materials=Materials(uo2,he,zr,h2o,ss,air,lead,copper,alu)
###Pins

fuel=Pin('1')
fuel.add_region((0.41,'1'))  #todo i should be able to refer with variable name to the material
fuel.add_region((0.42,'2'))
fuel.add_region((0.48,'3'))

waterchannel=Pin('2')
waterchannel.add_region((0.48,'4'))

rodguide=Pin('3')
rodguide.add_region((0.42,'4'))
rodguide.add_region((0.48,'3'))

pins=Pins(fuel,rodguide)
###Assembly

pwrOrig=Assembly(17,17)
pwrOrig.set_pitch(1.26)
pwrOrig._source=['1'] #to be fixed, add sourcePin or something like that!
pwrOrig.set_coolant('4')
pwrOrig.set_surrounding('6')
pwrOrig.set_pins(pins)

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
F5alu3mm.set_rectangle(Rectangle(Point(145.805, 202.374),Point(202.374, 145.805),
                                           Point(202.162, 145.593),Point(145.593, 202.162)))
F5alu3mm.set_material('9')
F5alu3mm.set_accommat('6')

F5cooper1mm=Absorber('F5cooper1mm')
F5cooper1mm.set_rectangle(Rectangle(Point(144.108, 200.677),Point(200.677, 144.108),
                                           Point(200.606, 144.0376),Point(144.0376, 200.606)))
F5cooper1mm.set_material('8')
F5cooper1mm.set_accommat('6')

F5lead8mm=Absorber('F5lead8mm')
F5lead8mm.set_rectangle(Rectangle(Point(146.37, 202.94),Point(202.94, 146.37),
                                           Point(202.374, 145.805),Point(145.805, 202.374)))
F5lead8mm.set_material('7')
F5lead8mm.set_accommat('6')

F5steel21mm=Absorber('F5steel21mm')
F5steel21mm.set_rectangle(Rectangle(Point(145.593, 202.162),Point(202.162, 145.593),
                                           Point(200.677, 144.108),Point(144.108, 200.677)))
F5steel21mm.set_material('5')
F5steel21mm.set_accommat('6')

detectors=Detectors(F5,F15)
absorbers=Absorbers(F5alu3mm,F5cooper1mm,F5lead8mm,F5steel21mm)
                
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
pwrClab.set_output('testOOP6.dat')
pwrClab.set_detectors(detectors)
pwrClab.set_absorbers(absorbers)
pwrClab.set_materials(materials)
start = time.time()
#for _ in range(10):
pwrClab.Run()
#end = time.time()
#print(end - start)

plt.figure()
plt.plot(pwrClab.elines,pwrClab._geomEff)
plt.show()

plt.figure()
plt.imshow(pwrClab._contributionMap['0.662'],cmap='jet')
plt.title('Energy=0.662')
plt.colorbar()
plt.show()
