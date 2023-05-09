import math 
from Gconstant import*

denwat = 998 # at 21 degrees C 
uwat = 8.90 * 10**-4 
#functions for the model 


#hetero-aggregation 

def Htaggre(alpha,kcoll,Cspm):
    kh = alpha*kcoll*Cspm
    
    return kh 

# where alpha is the attactchment efficiency, Cspm concn of suspended matter, Kcoll is the collisino rate constant, 

def Vsettle(denP, rP):
    v = (2*(denP - denwat)*9.81*(rP**2))/(9*uwat*denwat)
    
    return v 
def Vsetk(v,d):
    kv = v/d
    return kv 


def Kcoll(kb,Tw,r1,r2,G,v1,v2):
    kc1 = ((2*kb*Tw)*((r1 +r2)**2))/(3*uwat*(r1*r2))
    kc2 = 4*G*((r1+r2)**3)/3
    p = math.pi 
    kc3 = p*((r1+r2)**2)*abs(v1-v2)
    kcoll = kc1 +kc2 +kc3 
    
    return kcoll 


# rational method 

def RrOff(i,c,A):
    Q = i*c*A
    return Q

# degradation 

def Degradation(t_half_d):
    
    #degradation estimations
    """ relates only to MP & NPs. Full degradation probably extremely slow
    possibly not significant for most simulations. But add anyway for scenario
    analysis or biodegradable polymers. Values currently placeholders
    ! Add a size relation?!"""
    #degradation half-life of MPs used as input is in days
        
    #degradation rate constant 
    k_deg = math.log(2)/(t_half_d*24*60*60) 

    return k_deg


def Advec(Vflow, Across, Volflow):
    kflow = Vflow * (Across/Volflow)
    
    return kflow 




def Rainconvert(R,t):
    rain = (R/t) * 10**-3
    return rain 
    
def Mpflow(Mpc, In, Ac, Ti): # calculates flow of TWP on road in mass/m3
    Iw = In* Ac * Ti 
    C = Mpc *0.5 / (Iw)
    return C

Vsettle(1000, 0.3)

    