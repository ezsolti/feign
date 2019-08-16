from BUmuFunctions import *
import os
bumatfile0 = 'sBU0_pwr.bumat0'
bumatfile60 = 'sBU60_pwr.bumat0'


inv,conc = readInventory(bumatfile0)

massconcdic =  AtConc_to_ZWeightPer(inv,conc)

xcomfuelstr = XCOMmaterial(massconcdic)

xcomstr="'freshfuel\n4\n"+str(len(massconcdic))+"\n"+xcomfuelstr+"1\n3\n1\n34\n4.971E-01\n5.63E-01\n5.69E-01\n6.006E-01\n6.04E-01\n6.103E-01\n6.21E-01\n6.35E-01\n6.62E-01\n7.23E-01\n7.24E-01\n7.56E-01\n7.57E-01\n7.65E-01\n7.95E-01\n8.01E-01\n8.73E-01\n9.96E-01\n1.004E+00\n1.038E+00\n1.05E+00\n1.167E+00\n1.205E+00\n1.246E+00\n1.274E+00\n1.365E+00\n1.494E+00\n1.562E+00\n1.596E+00\n1.766E+00\n1.797E+00\n1.988E+00\n2.112E+00\n2.185E+00\nN\nfreshfuel.dat\n1\n'"

path=os.getcwd()
os.chdir('/home/zsolt/Documents/FEIGN/XCOM/')
os.system('printf '+xcomstr+' | ./XCOMtest')
os.chdir(path)

