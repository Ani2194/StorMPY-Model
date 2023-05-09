from Gconstant import *
import numpy as np
import math
from functions import Advec

# Flow 


class FlowSt(): 
    
    def __init__(self, name, length, Diameter):
        self.name = name
        self.length = length 
        self.Diameter = Diameter
        
        
   
    
    def calctheta(self,Q):
        lt = []
        li =[]
        for i in np.arange(0.1,360, 0.01):
            x = (0.849* C * self.Diameter**2.63 * (2*((i)) - math.sin((2*(i))) )** 1.63 * slope**0.54)/ (2* ((i)))**0.63
            lt.append(abs(Q-x))
            li.append((i))
        return li[lt.index((min(lt)))]
            
   
    def calcd(self,Q,theta):
        
       d = self.Diameter*(1 -math.cos((((theta)))))/2
       return d 
         
    def FlowV(self,d,Q,theta):
        a = ((self.Diameter/2)**2) *((2*theta) - math.sin((2*theta)))/2
        V = Q/a
        return V
        
    def Across(self,theta, d ):
        a = ((self.Diameter/2)**2)*((((2*theta)) - math.sin((2*theta))))/2
         
            
        return a 
    
    def CalVol(self,d, theta): 
        
        
        a = ((self.Diameter/2)**2) *((theta) - math.sin((theta)))/2
        Vol = a * self.length 
        
        return Vol 
    
    def TssConc(self):
        T1 = dfconcTSSOrganic[self.name == dfconcTSSOrganic['Sample']].index.values
        Tss = dfconcTSSOrganic.iloc[T1[0],1]
        return Tss
        
    def OrganicMC(self):
        Or1 = dfconcTSSOrganic[self.name == dfconcTSSOrganic['Sample']].index.values
        OrganicM = dfconcTSSOrganic.iloc[Or1[0],2]
        return OrganicM
        
    
        
        
            
        

class Well():
    
    def __init__(self,name,volume, Qin ):
        self.name = name 
        self.volume = volume
        self.Qin = Qin
         
        
    def OrganicMatterW(self):
        OrWm = dfconcTSSOrganic[self.name == dfconcTSSOrganic['Sample']].index.values
        OrganicMW = dfconcTSSOrganic.iloc[Or1[0],2]
        return OrganicMW
    
    def TssW(self):
        Tw1 = dfconcTSSOrganic[self.name == dfconcTSSOrganic['Sample']].index.values
        Tss = dfconcTSSOrganic.iloc[T1[0],1]
        return Tss
    
    def Retn(self): 
        rt = self.volume / self.Qin
        
        return round(rt)
        
        
        
                          
        
class Road():

    def __init__(self, name, area, conc, length,intensity, time):
        self.name = name 
        self.area = area 
        self.conc = conc
        self.length = length 
        self.intensity = intensity
        self.time = time 
        
        
    def calcQ(self,c):
        Q = c*self.intensity*self.area
        return Q
        
    def Vflow(self, Q):
        v = Q/self.area 
        
        return v 
    def ConT(self,Q): 
        c = self.conc * Q
        
        return c 
                        
   
        
        
#class OffRoad(): 


#Test class t o test functions 
StormW1 = FlowSt('Enkpinggully1', 100, 0.25)
theta1 = StormW1.calctheta(0.0036)
depth1 = StormW1.calcd(0.00363,theta1)
VelF = StormW1.FlowV(depth1, 0.12, theta1)

math.sin(0.52)