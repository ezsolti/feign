
import numpy as np
import os
import math

def floatErr(s):
    try:
        return float(s)
    except ValueError:
        return s
        
def readMu(path,column,energy):
    inputfile=open(path,'r').readlines()
    for line in inputfile:
        x=line.strip().split()
        if len(x)>=1 and floatErr(x[0])==energy:
            return float(x[column])

def readInventory(filename):
    """reads bumat file, and outputs list of ZAID and list of atomic concentration in [10²⁴/cm³]"""
    matfile=open(filename).readlines()
    inventory=[]
    concentration=[]
    #matfile = open(filename,'r')
    for line in matfile[6:]:
        x=line.strip().split()
        inventory.append(int(x[0][:-4]))
        concentration.append(float(x[1]))
    return np.array(inventory),np.array(concentration)
    
def AtConc_to_ZWeightPer(inventory,concentration):
    """the function expects list of isotop ZAIDs and serpent isotope concentration list in [10²⁴/cm³]
    the function works in three steps
    1, calculates the mass per cm3 for each isotope
    2, changes the ZAID into elements and sums the mass of each element
    3, returns the normalized mass (ie w%) for each element"""
    NA = 6.022140857E23
    masspervolume = {}
    Zprev=1
    massprev=0
    for iso, conc in zip(inventory,concentration):
        A = iso % 1000
        Z = (iso-A)/1000
        if A >= 300:
            if Z<80:
                A = A-200
            else:
                A = A-100
                    
        massconci = A*((conc*1e24)/NA)  #this gives the mass of that isotope in cm3
        
        if Z == Zprev:
            massprev = massprev+massconci
            Zprev=Z #doesnt make much sense:)
        else:
            masspervolume[elementsZtoName[Zprev]]=massprev
            Zprev=Z
            massprev=massconci
            
        
    #getting weight%
    summass=sum(masspervolume.values())
    for element in masspervolume:
        masspervolume[element]=masspervolume[element]/summass
    return masspervolume
    
def XCOMmaterial(massdic):
    #printf 'spentfuel\n4\n2\nH\n0.1\nO\n0.9\n1\n3\n1\n3\n0.6\n0.8\n0.9\nN\ntestauto.out\n1\n' | ./XCOMtest
    xcomstr=''    
    for element in massdic:
        xcomstr=xcomstr+element+'\n'+str(massdic[element])+'\n'
    return xcomstr
    
elementsZtoName={  109:"Mt",
            108: "Hs",
            107: "Bh",
            106: "Sg",
            105: "Db",
            104: "Rf",
            103: "Lr",
            102: "No",
            101: "Md",
            100: "Fm",
            99: "Es",
            98: "Cf",
            97: "Bk",
            96: "Cm",
            95: "Am",
            94: "Pu",
            93: "Np",
            91: "Pa",
            90: "Th",
            89: "Ac",
            88: "Ra",
            87: "Fr",
            86: "Rn",
            85: "At",
            84: "Po",
            83: "Bi",
            82: "Pb",
            81: "Tl",
            80: "Hg",
            79: "Au",
            78: "Pt",
            77: "Ir",
            76: "Os",
            75: "Re",
            73: "Ta",
            72: "Hf",
            71: "Lu",
            70: "Yb",
            69: "Tm",
            68: "Er",
            67: "Ho",
            66: "Dy",
            65: "Tb",
            64: "Gd",
            63: "Eu",
            62: "Sm",
            61: "Pm",
            60: "Nd",
            59: "Pr",
            58: "Ce",
            57: "La",
            56: "Ba",
            55: "Cs",
            54: "Xe",
            52: "Te",
            51: "Sb",
            50: "Sn",
            49: "In",
            48: "Cd",
            47: "Ag",
            46: "Pd",
            45: "Rh",
            44: "Ru",
            43: "Tc",
            42: "Mo",
            41: "Nb",
            40: "Zr",
            38: "Sr",
            37: "Rb",
            36: "Kr",
            35: "Br",
            34: "Se",
            33: "As",
            32: "Ge",
            31: "Ga",
            30: "Zn",
            29: "Cu",
            28: "Ni",
            27: "Co",
            26: "Fe",
            25: "Mn",
            24: "Cr",
            22: "Ti",
            21: "Sc",
            20: "Ca",
            18: "Ar",
            17: "Cl",
            14: "Si",
            13: "Al",
            12: "Mg",
            11: "Na",
            10: "Ne",
            4: "Be",
            3: "Li",
            2: "He",
            92: "U",
            74: "W",
            53: "I",
            39: "Y",
            23: "V",
            19: "K",
            18: "A",
            16: "S",
            15: "P",
            9: "F",
            8: "O",
            7: "N",
            6: "C",
            5: "B",
            1: "H"}