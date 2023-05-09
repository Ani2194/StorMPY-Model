import pandas as pd 
import numpy as np 
import math
from functions import*

# Constants for the model 

TwPSize = [20,50,80,100]
TwPDensity = 1800 # kg per meter cube 

Lsize = ['20', '50', '80', '100']

dfconcTWP = pd.read_csv(r'D:\Master thesis\Data\CurbData.csv')
dfconcTSSOrganic = pd.read_csv(r'D:\Master thesis\Data\TSS&OrganicM.csv')
dfRainsimulation = pd.read_csv(r'D:\Master thesis\Data\Rainfallsimulation.csv') # rainfall generator in m/s 

# Specification for stormwater sys
manningsc = 0.011
slope = 0.0022

r = 0.25 # in meters 
rn =  0.35 # in meters 

# hazen william equation constants 
k = 0.849  # for metric system 
C = 150  # for PVC pipes (roughness)


#specification for TSS and organic mater 

rTss = 5 * 10**-3
dTss = 2000   # in kg per meter cube 
rOrganic = 5 * 10 **-3
dOrganic = 1300 # in kg per meter cube 

# Constants for heteroaggregation 
kb = 1.38*10**-23 #Boltzmann constant k_B (in J/K)
Tw = 21 

# constants for settliing velcoity 

denwat = 998 # at 21 degrees C 
uwat = 8.90 * 10**-4  # at 20 degree C in kg/ms

# Areas of different sections on the roads ( to be measured and changed)



 #To compte S and Q for half capacity only if using manning and S is not constant i.e it involves energy 
def Qs():
    lq =[] 
    ls = []
    ldiffsq =[] 
    for i in np.arange(0.1, 3 , 0.0001):
       q = (i * manningsc * (2**(5/3)))/ r**(8/3)
       lq.append(i)
       for s in np.arange(0.0001 , 0.01 , 0.00001):
          s1 = math.pi * (s**1/2)
          ldiffsq.append(abs(q - s1))
          ls.append(s)
        
    Q = lq[ldiffsq.index(min(ldiffsq))//1000]      
    s = ls[ldiffsq.index(min(ldiffsq))]
    return (Q,s)
        
#Q123 = Qs()
#va = Mpflow(dfconcTWP.iloc[0,1],0.000044 , 300, 900) 
#en = Mpflow(dfconcTWP.iloc[0,2],0.000044 , 360, 900) 
#N1234 = 4*Mpflow(dfconcTWP.iloc[0,1],0.000044 , 500, 900)

#va1 = Mpflow(dfconcTWP.iloc[0,1],0.000001 , 300, 900)
#en1 = Mpflow(dfconcTWP.iloc[0,1],0.000001 , 360, 900)
#N12341 = 4*Mpflow(dfconcTWP.iloc[0,1],0.000001 , 500, 900)

