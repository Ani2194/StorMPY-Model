import seaborn as sns 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from sklearn import datasets
from sklearn.manifold import TSNE





TwPsize = [10,20,50,80,100]
RainSim = [10,20,40]
Allpipes = pd.read_csv('D:\\Master thesis\\Graphs\\Results\\ExcelR\\Allpipes.csv')
AllWells = pd.read_csv('D:\\Master thesis\\Graphs\\Results\\ExcelR\\AllWells.csv')

lcolAll = Allpipes.columns


def MxPtwp(nt,P9,P18,P27,f,dfM):
    ltemp =[] 
    for i in range(len(dfM)): 
        if dfM['TWPsize'][i] == nt:
            ltemp.append(i)
    lP9temp = []
    lP18temp =[]
    lP27temp =[]
    lPl = [lP9temp,lP18temp,lP27temp]
    lTr = [15,30,45]
    for z in ltemp: 
        lP9temp.append(dfM[P9][z])
        lP18temp.append(dfM[P18][z])
        lP27temp.append(dfM[P18][z])
    Mtemp =[] 
    Mtemp.append(f(lP9temp))
    Mtemp.append(f(lP18temp))
    Mtemp.append(f(lP27temp))
    PMt = f(Mtemp)
    Pipe = dfM['PipeName'][ltemp[lPl[Mtemp.index(PMt)].index(PMt)]]
    
    
    return (PMt , Pipe, (dfM['Rain(mm)'][ltemp[lPl[Mtemp.index(PMt)].index(PMt)]], lTr[Mtemp.index(PMt)]))

#MxPtwp(10, lcolAll[2], lcolAll[8], lcolAll[14],max)

def DfT(nP,num,f, dfM): 
    df5 = pd.DataFrame(TwPsize)
    df5.columns = ['TWPsize']
    df5[nP] = np.nan
    df5['Rain(mm)'] = np.nan
    df5['Time(mins)'] = np.nan
    df5['PipeName'] = np.nan
    for i in range(len(TwPsize)): 
        df5.iloc[i,1] = MxPtwp(TwPsize[i], lcolAll[num], lcolAll[num+7], lcolAll[num+14], f, dfM)[0]
        df5.iloc[i,2] = MxPtwp(TwPsize[i], lcolAll[num], lcolAll[num+7], lcolAll[num+14], f,dfM)[2][0]
        df5.iloc[i,3] = MxPtwp(TwPsize[i], lcolAll[num], lcolAll[num+7], lcolAll[num+14], f,dfM)[2][1]
        df5.iloc[i,4] = MxPtwp(TwPsize[i], lcolAll[num], lcolAll[num+7], lcolAll[num+14], f,dfM)[1]
        
    return df5

def TotalM(cn,dfM): 
    df5 = pd.DataFrame(RainSim)
    df5.columns = ['Rain(mm)']
    df5['15mins'] = np.nan
    df5['30mins'] = np.nan
    df5['45mins'] = np.nan
    for t in range(0,3):
        for z in range(len(RainSim)): 
           InRain =[]
           #InRain1 = []
           for i in range(len(dfM)): 
               if dfM['Rain(mm)'][i] == RainSim[z]:
                   if dfM.iloc[i,cn + (7*t)] == 'nan' :
                           InRain.append(0)
                   else : 
                       InRain.append(dfM.iloc[i,cn + (7*t)])
               #if dfM1['Rain(mm)'][i] == RainSim[z] :
                   #InRain1.append(dfM1.iloc[i,cn + (6*t)])
                   
           df5.iloc[z,t+1] = sum(InRain) #+ sum(InRain1)
    return df5
        

MsettleT = TotalM(8, Allpipes)  
HetroT = TotalM(2,Allpipes)  
PristT = TotalM(7,Allpipes)
MWsettleT = TotalM(8, AllWells)
MWhetroT = TotalM(2,AllWells)
MWpristT = TotalM(7,AllWells)
    

Htro = DfT('HetroTss(kg)', 2, max,Allpipes)
Htrom = DfT('HetroTss(kg)', 2, min,Allpipes)
Setl = DfT('MassSettle(kg)', 8, max,Allpipes)
Setlm = DfT('MassSettle(kg)', 8, min,Allpipes)
Prist = DfT('TWPprist', 7, max,Allpipes)
Pristm = DfT('TWPprist', 7, min,Allpipes)

Whtro = DfT('HetroTss(kg)', 2, max,AllWells)
Whtrom = DfT('HetroTss(kg)', 2, min,AllWells)
WSetl = DfT('MassSettle(kg)', 8, max,AllWells)
WSetlm = DfT('MassSettle(kg)', 8, min,AllWells)
WPrist = DfT('TWPprist', 7, max,AllWells)
WPristm = DfT('TWPprist', 7, min,AllWells)
        
def ToEx(df,p): 
    df.to_excel(p)           

ToEx(Htro,'D:\Master thesis\Graphs\Results\ExcelProcess\Hetero.xlsx' )   
ToEx(Htrom,'D:\Master thesis\Graphs\Results\ExcelProcess\Heterom.xlsx' ) 
ToEx(HetroT,'D:\Master thesis\Graphs\Results\ExcelProcess\HeteroT.xlsx' ) 
ToEx(MWhetroT,'D:\Master thesis\Graphs\Results\ExcelProcess\MWhetero.xlsx' )

ToEx(Setl,'D:\Master thesis\Graphs\Results\ExcelProcess\Setl.xlsx' )   
ToEx(Setlm,'D:\Master thesis\Graphs\Results\ExcelProcess\Setlm.xlsx' ) 
ToEx(MsettleT,'D:\Master thesis\Graphs\Results\ExcelProcess\MSetlT.xlsx' ) 
ToEx(MWsettleT,'D:\Master thesis\Graphs\Results\ExcelProcess\MWSetlT.xlsx' )
ToEx(Prist,'D:\Master thesis\Graphs\Results\ExcelProcess\prist.xlsx' ) 
ToEx(Pristm,'D:\Master thesis\Graphs\Results\ExcelProcess\pristm.xlsx' )


R20df = pd.DataFrame(Allpipes['Rain(mm)']) 
R20df.columns = ['Rain(mm)']
R20df['TWPsize'] = Allpipes['TWPsize']
R20df['18TWPhetro'] = Allpipes['18TWPhetro']
R20df['18HeteroTss(kg)'] = Allpipes['18HeteroTss(kg)']
R20df['18HeteroOrg(kg)'] = Allpipes['18HeteroOrg(kg)']
R20df['18TWPin'] = Allpipes['18TWPin']
R20df['18TWPout'] = Allpipes['18TWPout']
R20df['18TWPprist'] = Allpipes['18TWPprist']
R20df['18MassSettle(kg)'] = Allpipes['18MassSettle(kg)']
R20df['PipeName'] = Allpipes['PipeName']

R20df.reset_index(inplace = True)

lir = []
for i in range(len(R20df)): 
    if R20df.iloc[i,1] == 10 : 
        lir.append(i) 
    if R20df.iloc[i,1] == 40 : 
        lir.append(i)
R20df.drop(lir, axis = 0, inplace = True)    
R20df.drop([28,42,43,44], axis = 0 , inplace = True)   

plt.bar(R20df['PipeName'], R20df['18TWPhetro'])       
plt.xlabel('PipeName', fontsize = 20)                        
plt.ylabel('Hetero-aggregated TWP(kg)', fontsize = 20)  
plt.tick_params(labelsize = 18)                                

plt.bar(R20df['PipeName'], R20df['18MassSettle(kg)'])       
plt.xlabel('PipeName', fontsize = 20)                        
plt.ylabel('Settled TWP(kg)', fontsize = 20)
plt.tick_params(labelsize = 18)

plt.bar(R20df['PipeName'], R20df['18TWPprist'])       
plt.xlabel('PipeName', fontsize = 20)                        
plt.ylabel('Pristine TWP(kg)', fontsize = 20)
plt.tick_params(labelsize = 18)

R40df = pd.DataFrame(Allpipes['Rain(mm)']) 
R40df.columns = ['Rain(mm)']
R40df['TWPsize'] = Allpipes['TWPsize']
R40df['9TWPhetro'] = Allpipes['9TWPhetro']
R40df['9HeteroTss(kg)'] = Allpipes['9HeteroTss(kg)']
R40df['9HeteroOrg(kg)'] = Allpipes['9HeteroOrg(kg)']
R40df['9TWPin'] = Allpipes['9TWPin']
R40df['9TWPout'] = Allpipes['9TWPout']
R40df['9TWPprist'] = Allpipes['9TWPprist']
R40df['9MassSettle(kg)'] = Allpipes['9MassSettle(kg)']
R40df['PipeName'] = Allpipes['PipeName']



lir1 = []
for i in range(len(R40df)): 
    if R40df.iloc[i,0] == 10 : 
        lir1.append(i) 
    if R40df.iloc[i,0] == 20: 
        lir1.append(i)
R40df.drop(lir1, axis = 0, inplace = True)    
R40df.reset_index(inplace = True)

plt.bar(R40df['PipeName'], R40df['9TWPhetro'])       
plt.xlabel('PipeName', fontsize = 20)                        
plt.ylabel('Hetero-aggregated TWP(kg)', fontsize=20) 
plt.tick_params(labelsize = 18)

plt.bar(R40df['PipeName'], R40df['9MassSettle(kg)'])       
plt.xlabel('PipeName', fontsize= 20)                        
plt.ylabel('Settled TWP(kg)', fontsize= 20)
plt.tick_params(labelsize = 18)

plt.bar(R40df['PipeName'], R40df['9TWPprist'])       
plt.xlabel('PipeName', fontsize =20)                        
plt.ylabel('Pristine TWP(kg)', fontsize = 20)
plt.tick_params(labelsize = 18)

lpn = set(list((R20df['PipeName'])))


Newdf20 = pd.DataFrame(lpn)
Newdf20.columns = ['PipeName']
Newdf20['18TWPhetro'] = np.nan
Newdf20['18MassSettle(kg)'] = np.nan
Newdf20['18TWPprist'] = np.nan
for x in range(len(Newdf20['PipeName'])):
    lin = []
    for i in range(len(R20df['PipeName'])): 
         if Newdf20.iloc[x,0] == R20df.iloc[i,11 ]:
             lin.append(i)
    
    Newdf20['18TWPhetro'][x] = sum(R20df['18TWPhetro'][lin])   
    Newdf20['18MassSettle(kg)'][x] = sum(R20df['18MassSettle(kg)'][lin])
    Newdf20['18TWPprist'][x] = sum(R20df['18TWPprist'][lin])
    
        
R40df.iloc[9,10 ] = 'Natural2'

Newdf40 = pd.DataFrame(lpn)
Newdf40.columns = ['PipeName']
Newdf40['9TWPhetro'] = np.nan
Newdf40['9MassSettle(kg)'] = np.nan
Newdf40['9TWPprist'] = np.nan
Newdf40.iloc[6,0] = 'Natural2'
for x in range(len(Newdf40['PipeName'])):
    lin1 = []
    for i in range(len(R40df['PipeName'])): 
         if Newdf40.iloc[x,0] == R40df.iloc[i,10 ]:
             lin1.append(i)
    
    Newdf40['9TWPhetro'][x] = sum(R40df['9TWPhetro'][lin1])   
    Newdf40['9MassSettle(kg)'][x] = sum(R40df['9MassSettle(kg)'][lin1])
    Newdf40['9TWPprist'][x] = sum(R40df['9TWPprist'][lin1])    


x_pos = np.arange(len(Newdf40))
plt.bar(x_pos -0.2, Newdf20['18TWPhetro'], width = 0.4, label = '20mm30mins' )
plt.bar(x_pos +0.2, Newdf40['9TWPhetro'], width = 0.4, label = '40mm15mins')
plt.xticks(x_pos, Newdf40['PipeName'])
plt.xlabel('PipeNames', fontsize=17)
plt.ylabel('Hetro-aggegation(kg)', fontsize =17)
plt.tick_params(labelsize = 15)
plt.legend()

x_pos = np.arange(len(Newdf40))
plt.bar(x_pos -0.2, Newdf20['18MassSettle(kg)'], width = 0.4, label = '20mm30mins' )
plt.bar(x_pos +0.2, Newdf40['9MassSettle(kg)'], width = 0.4, label = '40mm15mins')
plt.xticks(x_pos, Newdf40['PipeName'])
plt.xlabel('PipeNames', fontsize = 17)
plt.ylabel('MassSettle(kg)', fontsize = 17)
plt.tick_params(labelsize = 15)
plt.legend()

x_pos = np.arange(len(Newdf40))
plt.bar(x_pos -0.2, Newdf20['18TWPprist'], width = 0.4, label = '20mm30mins' )
plt.bar(x_pos +0.2, Newdf40['9TWPprist'], width = 0.4, label = '40mm15mins')
plt.xticks(x_pos, Newdf40['PipeName'])
plt.xlabel('PipeNames', fontsize = 17)
plt.ylabel('TWPprist(kg)', fontsize = 17)
plt.tick_params(labelsize = 15)
plt.legend()