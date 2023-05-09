import numpy as np 
from Gconstant import *
import random 
import pandas as pd 
import math



def TWPgenerator(d):
         Percent = [35,25,25,15]
         TWPSi = pd.DataFrame(Percent)
         TWPSi.columns = ['Percent']
         TWPSi['Size'] = np.nan
         TWPSi['Conc(gm/m2)'] = np.nan
         for i in range(len(TWPSi['Size'])):
             TWPSi['Size'][i] = TwPSize[i]
             TWPSi['Conc(gm/m2)'][i] =  (dfconcTWP.iloc[d,1])* (TWPSi['Percent'][i])/100
         return TWPSi

    
class TWP():
    
    def __init__(self, size):
        self.size = size 
        #self.section = section # provision made if the snow data comes from elly
        
        
        
    def Num(self, MassT, df):
        if self.size == 20 :
            mass = MassT * df.iloc[0,0]/ 100
            Vol1 = (4/3) * math.pi * (20 * 10**-6)**3
            num = (mass * TwPDensity) / Vol1 
            return num 
            
        if self.size == 50 :
            mass = MassT * df.iloc[1,0]/ 100
            Vol1 = (4/3) * math.pi * (50 * 10**-6)**3
            num = (mass * TwPDensity) / Vol1   
            return num 
        if self.size == 80 :
            mass = MassT * df.iloc[2,0]/ 100
            Vol1 = (4/3) * math.pi * (80 * 10**-6)**3
            num = (mass * TwPDensity) / Vol1 
            
            return num 
        if self.size == 100 :
            mass = MassT * df.iloc[3,0]/ 100
            Vol1 = (4/3) * math.pi * (100 * 10**-6)**3
            num = (mass * TwPDensity) / Vol1   
            return num 
        
    def NumSm(self, MassT):
        if self.size == 10 :
            mass = MassT 
            Vol1 = (4/3) * math.pi * (10 * 10**-6)**3
            num = (mass * TwPDensity) / Vol1 
            return num
        
    def Mass(self, numb):
        if self.size == 20 :
            
            Vol1 = (4/3) * math.pi * (20 * 10**-6)**3
            mass = numb * Vol1 / TwPDensity 
            return mass 
            
        if self.size == 50 :

            Vol1 = (4/3) * math.pi * (50 * 10**-6)**3
            mass = numb * Vol1 / TwPDensity   
            return mass 
        if self.size == 80 :
            
            Vol1 = (4/3) * math.pi * (80 * 10**-6)**3
            mass = numb * Vol1 / TwPDensity 
            
            return mass 
        if self.size == 100 :
            
            Vol1 = (4/3) * math.pi * (100 * 10**-6)**3
            mass = numb * Vol1 / TwPDensity  
            return mass 
        
        if self.size == 10 :
            
            Vol1 = (4/3) * math.pi * (20 * 10**-6)**3
            mass = numb * Vol1 / TwPDensity 
            return mass
#example to see if the function works
# oppo = TWPgenerator(0)        
        



