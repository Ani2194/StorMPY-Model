from Gconstant import *
from functions import *
from TWPGen import *
from FLowS import * 
import pandas as pd 
import numpy as np

# generating the scenario
#Rain fall 
Rf = dfRainsimulation.iloc[2,3] # in m/ second 
TRf = dfRainsimulation.iloc[3,3] # TRf must be consistent with Rf 

#TWP for vasteros 
Twp1 = TWPgenerator(0)
Twpcrva = Mpflow(dfconcTWP.iloc[0,1], Rf, 300, TRf)

TWPl = [TWP(20), TWP(50), TWP(80), TWP(100)]


# calculating settling velocity 
VsettleTWP = []
#settleTWPk = []
for i in range(len(TWPl)): 
    VsettleTWP.append(Vsettle(TwPDensity, (TWPl[i].size) * 10**-6))
    #settleTWPk.append(Settlet(VsettleTWP[i], den))
VsettleOrganic = Vsettle(dOrganic,rOrganic)
VsettleTss = Vsettle(dTss,rTss)
Vs10 = Vsettle(TwPDensity, TWP(10).size * 10**-6)
# functinon for calculating rate constant for heteroaggregation 
def hetrok(G): 
    HeteroTssTWPlk = []
    HeteroOrganTWPlk = [] 
    for i in range(len(TWPl)):
        kHetroTssva = 0.9 * Kcoll(kb,Tw,(TWPl[i].size)*10**-6, rTss,G,VsettleTWP[i], VsettleTss )
        kHetroOrgva = 0.038* Kcoll(kb,Tw,(TWPl[i].size)*10**-6, rOrganic,G,VsettleTWP[i],VsettleOrganic)
        HeteroTssTWPlk.append(kHetroTssva)
        HeteroOrganTWPlk.append(kHetroOrgva)
    return (HeteroTssTWPlk,HeteroOrganTWPlk)

def hetrok10(G):
    l =[]
    kHetroTssva = 0.9 *Kcoll(kb,Tw,(10)*10**-6, rTss,G,Vs10, VsettleTss )
    kHetroOrgva = 0.038* Kcoll(kb,Tw,(10)*10**-6, rOrganic,G,Vs10,VsettleOrganic)
    l.append(kHetroTssva)
    l.append(kHetroOrgva)
    return l
    

# simulatino for the vasteros gully pot 

RoadVa = Road('Va', 300, Twpcrva, 50,Rf,TRf )
Qva = RoadVa.calcQ(1) 
MassTwpTva = RoadVa.ConT(Qva)
StorMva = FlowSt('Vasterasgully1', 50, 0.25)   
thetaVa = StorMva.calctheta(Qva)
dva = StorMva.calcd(Qva,thetaVa)
Vva = StorMva.FlowV(dva, Qva,thetaVa)
G2 = Vva/dva
Tva = StorMva.length/Vva

Numlva =[]
ksetv = []
for i in range(len(TWPl)):
    Numlva.append(TWPl[i].Mass(TWPl[i].Num(MassTwpTva,Twp1 )) *TRf)
    ksetv.append(Vsetk(VsettleTWP[i],dva))

Hvak = hetrok(G2)  # heteroaggregatino rate constant 
 
TWPva = pd.DataFrame(Lsize)
TWPva.columns = ['TWPsize']
TWPva['HeteroTss(kg)'] = np.nan
TWPva['HeteroOrg(kg)'] = np.nan
TWPva['TWPhetro'] = np.nan
TWPva['TWPin'] = Numlva
TWPva['TWPout'] = np.nan
TWPva['TWPprist'] = np.nan
TWPva['MassSettle(kg)'] = np.nan
for i in range(len(TWPva)) : 
    TWPva['HeteroTss(kg)'][i] = Numlva[i]  * Hvak[0][i]*Tva
    TWPva['TWPhetro'][i] = TWPva['HeteroTss(kg)'][i]
    TWPva['HeteroOrg(kg)'][i] = Numlva[i]  * Hvak[1][i] * 0.5*Tva
    if TWPva['TWPin'][i] *ksetv[i] *Tva >= TWPva['TWPin'][i]:
        TWPva['MassSettle(kg)'][i] =  TWPva['TWPin'][i]
    else: 
       TWPva['MassSettle(kg)'][i] = (TWPva['TWPin'][i] *ksetv[i] *Tva)
    if TWPva['TWPin'][i] - TWPva['MassSettle(kg)'][i] < 0 :
         TWPva['TWPout'][i] = 0
    else :
        TWPva['TWPout'][i] = TWPva['TWPin'][i] - TWPva['MassSettle(kg)'][i]
    if TWPva['TWPout'][i] - TWPva['HeteroTss(kg)'][i] - TWPva['HeteroOrg(kg)'][i] < 0 :
        TWPva['TWPprist'][i] = 0
    else : 
        TWPva['TWPprist'][i] = TWPva['TWPout'][i] - TWPva['HeteroTss(kg)'][i] - TWPva['HeteroOrg(kg)'][i]
    
          
#AdvecVa = Advec(StorMva.FlowV(dva, Qva,thetaVa), StorMva.Across(thetaVa,dva), StorMva.CalVol(dva, thetaVa)) * MassTwpTva 
LossMassva = sum(TWPva['MassSettle(kg)']) 
# check if advec is less than Lossmass 
TotalMTva = MassTwpTva*TRf - LossMassva

# Simulation for the enkoping gully
Twpcren = Mpflow(dfconcTWP.iloc[0,1], Rf, 360, TRf)
RoadEn = Road('En',360,Twpcren, 15, Rf, TRf)
Qen = RoadEn.calcQ(1) + Qva 
MassTwpTen = RoadEn.ConT(Qen) #+ TotalMTva
StorMen = FlowSt('Enkpinggully1', 10,0.25)
   
thetaEn = StorMen.calctheta(Qen)
den = StorMen.calcd(Qen,thetaEn)
Ven = StorMen.FlowV(den, Qen,thetaEn)
G1 = Ven/den # used for hetero aggrgation 
Ten = StorMen.length/Ven

kseten =[]
Numlen =[]
for i in range(len(TWPl)):
    Numlen.append((TWPl[i].Mass(TWPl[i].Num(MassTwpTen,Twp1 ))) *TRf)
    kseten.append(Vsetk(VsettleTWP[i],den))
     
Henk = hetrok(G1)

TWPen = pd.DataFrame(Lsize)
TWPen.columns = ['TWPsize']
TWPen['HeteroTss(kg)'] = np.nan
TWPen['TWPin'] = np.nan
TWPen['TWPhetro'] = np.nan
TWPen['TWPout'] = np.nan
TWPen['HeteroOrg(kg)'] = np.nan
TWPen['MassSettle(kg)'] = np.nan
TWPen['TWPprist'] = np.nan
for i in range(len(TWPva)) : 
    TWPen['TWPin'][i] = Numlen[i] + TWPva['TWPout'][i]
    TWPen['TWPhetro'][i] = (Numlen[i] * Henk[0][i]*Ten) + (TWPva['TWPprist'][0]*Henk[0][0]*Ten)
    TWPen['HeteroTss(kg)'][i] = TWPen['TWPhetro'][i] + TWPva['HeteroTss(kg)'][i]
    TWPen['HeteroOrg(kg)'][i] = (Numlen[i] * Henk[1][i] * 0.5*Ten) +(TWPva['TWPprist'][i]*Henk[1][i]*Ten)+ TWPva['HeteroOrg(kg)'][i]
    if TWPen['TWPin'][i] *ksetv[i] *Tva >= TWPen['TWPin'][i]:
        TWPen['MassSettle(kg)'][i] = TWPen['TWPin'][i]
    else: 
       TWPen['MassSettle(kg)'][i] = (TWPen['TWPin'][i] *kseten[i] *Ten)
    if TWPen['TWPin'][i] - TWPen['MassSettle(kg)'][i] < 0 :
         TWPen['TWPout'][i] = 0
    else :
        TWPen['TWPout'][i] = TWPen['TWPin'][i] - TWPen['MassSettle(kg)'][i]
    if TWPen['TWPout'][i] - TWPen['HeteroTss(kg)'][i] - TWPen['HeteroOrg(kg)'][i] < 0 :
        TWPen['TWPprist'][i] = 0
    else : 
        TWPen['TWPprist'][i] = TWPen['TWPout'][i] - TWPen['HeteroTss(kg)'][i] - TWPen['HeteroOrg(kg)'][i]
    

               
#AdvecEnk = Advec(StorMen.FlowV(den, Qen,thetaEn[0]), StorMen.Across(thetaEn[0],den), StorMen.CalVol(den, thetaEn[0])) * MassTwpT
LossMassen = sum(TWPen['MassSettle(kg)']) 

TotalMTen = MassTwpTen - LossMassen

# natural pathway besides road side 
Twpsm1 = Mpflow(dfconcTWP.iloc[0,2], Rf,500,TRf )

Natural1 = Road('1', 500,Twpsm1,68.9, Rf,TRf )
QN1 = Natural1.calcQ(1)
MassNa1 = Natural1.ConT(QN1) 
StorMN1 = FlowSt('Natural1', 68.9,0.25)
thetaN1 = StorMN1.calctheta(QN1) # change discharge after consultation 
dN1 = StorMN1.calcd(QN1,thetaN1)
VN1 = StorMN1.FlowV(dN1, QN1,thetaN1)
GN1 = VN1/dN1
TN1 = StorMN1.length/VN1
HeN1 = hetrok10(G1)

NumlN1 = MassNa1 *TRf
ksetN1 = (Vsetk(Vs10,dN1))

TotalMN1 = MassNa1 - MassNa1*ksetN1


TWPN1in = NumlN1
if (TWPN1in *ksetN1*TN1) >= TWPN1in : 
    TWPN1MassSet = TWPN1in
else : 
    TWPN1MassSet = (TWPN1in *ksetN1*TN1)
    
TWPN1hetroTss = (NumlN1 * HeN1[0]*TN1)
TWPN1hetroOrg = (NumlN1 * HeN1[1] * 0.5*TN1)
if TWPN1in - TWPN1MassSet < 0 : 
     TWPN1out = 0
else :
   TWPN1out = TWPN1in - TWPN1MassSet
if TWPN1out - TWPN1hetroOrg - TWPN1hetroTss < 0 : 
    TWPN1prist = 0 
else : 
   TWPN1prist = TWPN1out - TWPN1hetroOrg - TWPN1hetroTss


Natural2 = Road('2', 632.3,Twpsm1,10, Rf,TRf )
QN2 = Natural2.calcQ(1) + QN1
MassNa2 = Natural2.ConT(QN2)
StorMN2 = FlowSt('Natural2', 10,0.25)
thetaN2 = StorMN2.calctheta(QN2) 
dN2 = StorMN2.calcd(QN2,thetaN2)
VN2 = StorMN2.FlowV(dN2, QN2,thetaN2)
GN2 = VN2/dN2
TN2 = StorMN2.length/VN2
HeN2 = hetrok10(GN2)

NumlN2 = MassNa2 *TRf
ksetN2 = (Vsetk(Vs10,dN2)) 

TotalMN2 = MassNa2 - MassNa2*ksetN2

TWPN2in = NumlN2 + TWPN1out
if (TWPN2in *ksetN2*TN2) >= TWPN2in : 
    TWPN2MassSet = TWPN2in 
else : 
    TWPN2MassSet = (TWPN2in *ksetN2*TN2)
TWPN2hetro =  (NumlN2 +TWPN1prist) * HeN2[0]*TN2
TWPN2hetroTss = TWPN2hetro  + TWPN1hetroTss
TWPN2hetroOrg = (NumlN2  + TWPN1prist) * HeN2[1] * 0.5 * TN2 + TWPN1hetroOrg
if TWPN2in - TWPN2MassSet < 0 : 
     TWPN2out = 0
else :
   TWPN2out = TWPN2in - TWPN2MassSet
if TWPN2out - TWPN2hetroOrg - TWPN2hetroTss < 0 : 
    TWPN2prist = 0 
else : 
   TWPN2prist = TWPN2out - TWPN2hetroOrg - TWPN2hetroTss


Natural3 = Road('3', 500,Twpsm1,68.9, Rf,TRf )
QN3 = Natural3.calcQ(1)
MassNa3 = Natural3.ConT(QN3) 
StorMN3 = FlowSt('Natural3', 68.9,0.25)
thetaN3 = StorMN1.calctheta(QN3) # change discharge after consultation 
dN3 = StorMN3.calcd(QN3,thetaN3)
VN3 = StorMN3.FlowV(dN3, QN3,thetaN3)
GN3 = VN3/dN1
TN3 = StorMN3.length/VN3
HeN3 = hetrok10(GN3)
NumlN3 = MassNa3 * TRf
ksetN3 = (Vsetk(Vs10,dN3))

TWPN3in = NumlN3
if (TWPN3in *ksetN3*TN3) >= TWPN3in : 
    TWPN3MassSet = TWPN3in
else : 
    TWPN3MassSet = (TWPN3in *ksetN3*TN3)

TWPN3hetroTss = (NumlN3 * HeN3[0]*TN3)
TWPN3hetroOrg = (NumlN3 * HeN3[1] * 0.5*TN3)

if TWPN3in - TWPN3MassSet < 0 : 
     TWPN3out = 0
else :
   TWPN3out = TWPN3in - TWPN3MassSet
if TWPN3out - TWPN3hetroOrg - TWPN3hetroTss < 0 : 
    TWPN3prist = 0 
else : 
   TWPN3prist = TWPN3out - TWPN3hetroOrg - TWPN3hetroTss


TotalMN3 = MassNa3 - MassNa3*ksetN3

Natural4 = Road('2', 770,Twpsm1,10, Rf,TRf )
QN4 = Natural4.calcQ(1) + QN3
MassNa4 = Natural4.ConT(QN4)
StorMN4 = FlowSt('Natural4', 10,0.25)
thetaN4 = StorMN4.calctheta(QN4) 
dN4 = StorMN4.calcd(QN4,thetaN4)
VN4 = StorMN4.FlowV(dN4, QN4,thetaN4)
GN4 = VN4/dN4
TN4 = StorMN4.length/VN4
HeN4 = hetrok10(GN4)

NumlN4 = MassNa4 * TRf
ksetN4 = (Vsetk(Vs10,dN4)) 

TWPN4in = NumlN4 + TWPN3out
TWPN4MassSet = (TWPN4in *ksetN4*TN4)
if (TWPN4in *ksetN4*TN4) >= TWPN4in : 
    TWPN4MassSet = TWPN4in
else : 
    TWPN4MassSet = (TWPN4in *ksetN4*TN4)
TWPN4hetro = (NumlN4 +TWPN3prist) * HeN4[0]*TN4
TWPN4hetroTss =  TWPN4hetro + TWPN3hetroTss
TWPN4hetroOrg = (NumlN4  + TWPN3prist) * HeN4[1] * 0.5 * TN4 + TWPN3hetroOrg
if TWPN4in - TWPN4MassSet < 0 : 
     TWPN4out = 0
else :
   TWPN4out = TWPN4in - TWPN4MassSet
if TWPN4out - TWPN4hetroOrg - TWPN4hetroTss < 0 : 
    TWPN4prist = 0 
else : 
   TWPN4prist = TWPN4out - TWPN4hetroOrg - TWPN4hetroTss


TotalMN4 = MassNa4 - MassNa4*ksetN4

TWPNa = pd.DataFrame(['Natural1', 'Natural2', 'Natural3','Natural4'])
TWPNa.columns = ['Pathway Name']
TWPNa['TWPin'] = [TWPN1in,TWPN2in,TWPN3in,TWPN4in ] 
TWPNa['TWPhetro'] = [TWPN1hetroTss, TWPN2hetro, TWPN3hetroTss, TWPN4hetroTss ]
TWPNa['HeteroOrg(kg)'] = [TWPN1hetroOrg,TWPN2hetroOrg, TWPN3hetroOrg, TWPN4hetroOrg]
TWPNa['HeteroTss(kg)'] =[TWPN1hetroTss, TWPN2hetroTss, TWPN3hetroTss, TWPN4hetroTss]
TWPNa['MassSettle(kg)'] = [TWPN1MassSet, TWPN2MassSet, TWPN3MassSet, TWPN4MassSet ]
TWPNa['TWPout'] = [TWPN1out,TWPN2out,TWPN3out,TWPN4out]
TWPNa['TWPprist'] = [TWPN1prist, TWPN2prist, TWPN3prist, TWPN4prist]

# Simulating Wells 
# Well A
Wa = Well('A', 0.062,QN2)
ksetWA = (Vsetk(Vs10, 0.35)) * Wa.Retn()
NumlWa = TWPN2out 
HeWa = hetrok10(VN2/0.35) * Wa.Retn()

TWPWain = NumlWa
TWPWaMassSet = (TWPWain *ksetWA)
TWPWahetro = (TWPWain * HeWa[0]*Wa.Retn())
TWPWahetroTss = TWPWahetro + TWPN2hetroTss
TWPWahetroOrg = (TWPWain * HeWa[1] * 0.5*Wa.Retn()) + TWPN2hetroOrg
TWPWaout = TWPWain - TWPWaMassSet
TWPWaprist = TWPWaout - TWPWahetroOrg - TWPWahetroTss

#Well C
Wc = Well('C',0.062,QN4)
ksetWC = (Vsetk(Vs10,0.35))
NumlWc = TWPN4out
HeWc = hetrok10(VN4/0.35)

TWPWcin = NumlWc
TWPWcMassSet = (TWPWain *ksetWC)
TWPWchetro = (TWPWcin * HeWc[0]*Wc.Retn())
TWPWchetroTss =  TWPWchetro + TWPN2hetroTss
TWPWchetroOrg = (TWPWcin * HeWc[1] * 0.5*Wc.Retn()) + TWPN2hetroOrg
TWPWcout = TWPWcin - TWPWcMassSet
TWPWcprist = TWPWcout - TWPWchetroOrg - TWPWchetroTss

TWPWac = pd.DataFrame(['A', 'C']) 
TWPWac.columns = ['Well name']
TWPWac["TWPin"] = [TWPWain,TWPWcin]
TWPWac['MassSettle(kg)'] = [TWPWaMassSet, TWPWcMassSet]
TWPWac['TWPhetro'] = [TWPWahetro, TWPWchetro]
TWPWac['HeteroTss(kg)']= [TWPWahetroTss, TWPWchetroTss]
TWPWac['HeteroOrg(kg)'] = [TWPWahetroOrg, TWPWchetroOrg]
TWPWac['TWPout'] = [TWPWaout,TWPWcout]
TWPWac['TWPprist'] = [TWPWaprist, TWPWcprist]


# Well B 
Wb = Well('B',0.062,Qen)
HeWb = hetrok(Ven/0.35)
MassWb = TotalMTen * TRf



ksetWB =[] 
 
for i in range(len(TWPl)):
    ksetWB.append(Vsetk(VsettleTWP[i],0.35))
    
    
TWPWb = pd.DataFrame(Lsize)
TWPWb.columns = ['TWPsize']
TWPWb['TWPin'] = np.nan
TWPWb['TWPhetro'] = np.nan
TWPWb['HeteroTss(kg)'] = np.nan
TWPWb['HeteroOrg(kg)'] = np.nan
TWPWb['TWPout'] = np.nan 
TWPWb['MassSettle(kg)'] = np.nan
TWPWb['TWPprist'] = np.nan
for i in range(0,4):
    TWPWb['TWPin'][i] = TWPen['TWPin'][i] 
    TWPWb['MassSettle(kg)'][i] = (TWPWb['TWPin'][i] *ksetWB[i])
    TWPWb['TWPout'][i] = TWPWb['TWPin'][i] - TWPWb['MassSettle(kg)'][i]
    TWPWb['TWPhetro'][i] = (TWPen['TWPprist'][i]* HeWb[0][i] * Wb.Retn())
    TWPWb['HeteroTss(kg)'][i] =  TWPWb['TWPhetro'][i] + TWPen['HeteroTss(kg)'][i]
    TWPWb['HeteroOrg(kg)'][i] = (TWPen['TWPprist'][i] * HeWb[1][i] * 0.5 * Wb.Retn()) + TWPen['HeteroOrg(kg)'][i]
    TWPWb['TWPprist'][i] = TWPWb['TWPout'][i] - TWPWb['HeteroTss(kg)'][i] - TWPWb['HeteroOrg(kg)'][i]
    
    


#Well D 
Qd = QN2 + QN4 + Qen
Wd = Well('D', 0.703, Qd )
Vd = Qd/1.7
HeWd = hetrok(Vd/0.35)
HeWd10 = hetrok10(Vd/0.35)

ksetWD = [] 
for i in range(len(TWPl)):
    ksetWD.append(Vsetk(VsettleTWP[i], 0.35) * Wd.Retn())
    
ksetWD.append(Vsetk(Vs10,0.35) * Wd.Retn())
timel = [Tva+Ten, TN1 +TN2, TN3+TN4]


TWPWd = pd.DataFrame([20,50,80,100,10])
TWPWd.columns = ['TWPsize']
TWPWd['TWPin'] = np.nan 
TWPWd['TWPout'] = np.nan
TWPWd['TWPhetro'] = np.nan
TWPWd['HeteroTss(kg)'] = np.nan
TWPWd['HeteroOrg(kg)'] = np.nan
TWPWd['MassSettle(kg)']= np.nan
TWPWd['TWPprist'] = np.nan
for i in range(0,4):
    TWPWd['TWPin'][i] = TWPWb['TWPout'][i]                      
    TWPWd['MassSettle(kg)'][i] = (TWPWd['TWPin'][i] *ksetWD[i])
    TWPWd['TWPhetro'][i] = TWPWb['TWPprist'][i] * HeWd[0][i] * Wd.Retn()
    TWPWd['HeteroTss(kg)'][i] = TWPWd['TWPhetro'][i] + TWPWb['HeteroTss(kg)'][i]
    TWPWd['HeteroOrg(kg)'][i] = TWPWb['TWPprist'][i] * (HeWd[1][i]) * 0.5 * Wd.Retn()  + TWPWb['HeteroOrg(kg)'][i]
    TWPWd['TWPout'][i] = TWPWd['TWPin'][i] - TWPWd['MassSettle(kg)'][i]
    TWPWd['TWPprist'][i] = TWPWd['TWPout'][i] - TWPWd['HeteroTss(kg)'][i] - TWPWd['HeteroOrg(kg)'][i]
    

TWPWd['TWPin'][4] = sum(TWPWac['TWPout'])
TWPWd['TWPhetro'][4] = sum(TWPWac['TWPprist']) * HeWd10[0]* Wd.Retn()
TWPWd['HeteroTss(kg)'][4] = TWPWd['TWPhetro'][4] + sum(TWPWac['HeteroTss(kg)'])
TWPWd['HeteroOrg(kg)'][4] = sum(TWPWac['TWPprist']) * HeWd10[1]*Wd.Retn() + sum(TWPWac['HeteroOrg(kg)'])
TWPWd['MassSettle(kg)'][4] = TWPWd['TWPin'][4] * ksetWD[4]
TWPWd['TWPout'][4] = TWPWd['TWPin'][4] - TWPWd['MassSettle(kg)'][4]
TWPWd['TWPprist'][4] = TWPWd['TWPout'][4] - TWPWd['HeteroOrg(kg)'][4] - TWPWd['HeteroTss(kg)'][4]


# last pipe in the system 
StorMLa = FlowSt('Last1', 100, 0.35)
Qla = Qd +0.01
MassTwpTLa = sum(TWPWd['TWPout'])

thetaLa = StorMLa.calctheta(Qla)
dla = StorMLa.calcd(Qla,thetaLa)
Vla = StorMLa.FlowV(dla, Qla,thetaLa)
G4 = Vla/dla # used for hetero aggrgation 

Tla = StorMLa.length/ Vla

ksetla =[]

for i in range(len(TWPl)):
    ksetla.append(Vsetk(VsettleTWP[i],dla))
ksetla10 = Vsetk(Vs10, dla)
    
HeLa = hetrok(G4)
HeLa10 = hetrok10(G4)
Lsize5 = [20,50,80,100,10]

TWPLa = pd.DataFrame(Lsize5)
TWPLa.columns = ['TWPsize']
TWPLa['HeteroTss(kg)'] = np.nan
TWPLa['HeteroOrg(kg)'] = np.nan
TWPLa['TWPhetro'] = np.nan
TWPLa['TWPin'] = np.nan
TWPLa['MassSettle(kg)'] = np.nan
TWPLa['TWPout'] = np.nan
TWPLa['TWPprist'] = np.nan
for i in range(len(Lsize5) -1) : 
    TWPLa['TWPin'][i]= TWPWd['TWPout'][i] 
    TWPLa['TWPhetro'][i] = TWPWd['TWPprist'][i]*Tla*HeLa[0][i]
    TWPLa['HeteroTss(kg)'][i] =  TWPLa['TWPhetro'][i] + TWPWd['HeteroTss(kg)'][i]
    TWPLa['HeteroOrg(kg)'][i] = TWPWd['TWPprist'][i]*Tla*HeLa[1][i] + TWPWd['HeteroOrg(kg)'][i]
    TWPLa['MassSettle(kg)'][i] = TWPLa['TWPin'][i]* Tla * ksetla[i]
    if TWPLa['TWPin'][i]* Tla * ksetla[i] >= TWPLa['TWPin'][i] : 
        TWPLa['MassSettle(kg)'][i] = TWPLa['TWPin'][i]
    else :
        TWPLa['MassSettle(kg)'][i] = TWPLa['TWPin'][i]* Tla * ksetla[i]
        
    if TWPLa['TWPin'][i] - TWPLa['MassSettle(kg)'][i] < 0 :
         TWPLa['TWPout'][i] = 0
    else :
        TWPLa['TWPout'][i] = TWPLa['TWPin'][i] - TWPLa['MassSettle(kg)'][i]
    if TWPLa['TWPout'][i] - TWPLa['HeteroTss(kg)'][i] - TWPLa['HeteroOrg(kg)'][i] < 0 :
        TWPLa['TWPprist'][i] = 0
    else : 
        TWPLa['TWPprist'][i] = TWPLa['TWPout'][i] - TWPLa['HeteroTss(kg)'][i] - TWPLa['HeteroOrg(kg)'][i]
        
TWPLa['TWPhetro'][4] = TWPWd['TWPprist'][4] * HeLa10[0] * Tla
TWPLa['HeteroTss(kg)'][4] =  TWPLa['TWPhetro'][4] + TWPWd['HeteroTss(kg)'][4]
TWPLa['HeteroOrg(kg)'][4] = TWPWd['TWPprist'][4] * HeLa10[1] * Tla + TWPWd['HeteroOrg(kg)'][4]
TWPLa['TWPin'][4] = TWPWd['TWPin'][4]
TWPLa['MassSettle(kg)'][4] = TWPLa['TWPin'][4] * ksetla10 * Tla 
TWPLa['TWPout'][4] = TWPWd['TWPin'][4] - TWPLa['MassSettle(kg)'][4]
TWPLa['TWPprist'][4] = TWPLa['TWPout'][4] - TWPLa['HeteroTss(kg)'][4] - TWPLa['HeteroOrg(kg)'][4]
