from simulator import * 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
# comment all sections before using this section and get the results one by one. 


L = [StorMva.name, StorMen.name, StorMN1.name, StorMN2.name, StorMN3.name, StorMN4.name, StorMLa.name]
V = [Vva, Ven, VN1, VN2, VN3, VN4, Vla]
Df = [dva, den, dN1, dN2, dN3, dN4, dla]
Qf = [Qva, Qen, QN1, QN2, QN3,QN4,Qla ]

DfTWP = [TWPva,TWPen,TWPNa,TWPWac,TWPWb,TWPWd,TWPLa]
                                  
def PdStprop():
     Veldf = pd.DataFrame(L)
     Veldf.columns = ['StormwaterPipes']
     Veldf['Velocity(m/s)'] = np.nan
     Veldf['Depth(m)'] = np.nan
     Veldf['Discharge(m3/s)'] = np.nan
     for i in range(len(L)): 
         Veldf['Velocity(m/s)'][i] = V[i]
         Veldf['Depth(m)'][i] = Df[i]
         Veldf['Discharge(m3/s)'][i] = Qf[i]
         
     return Veldf
 
def LTwp(ldf):
    toi = ldf 
    return toi 
    


# will have to get results one by one, hence have to comment all other functions not in use        
#Flp10t9 = PdStprop()
#Flp10t18 = PdStprop()
#Flp10t27 = PdStprop()
#Flp20t9 = PdStprop()
#Flp20t18 = PdStprop()
#Flp20t27 = PdStprop()
#Flp40t9 = PdStprop()
#Flp40t18 = PdStprop()
#Flp40t27 = PdStprop()

#TWP10t9 = LTwp(DfTWP)
#TWP10t18 = LTwp(DfTWP)
#TWP10t27 =  LTwp(DfTWP)
#TWP20t9  = LTwp(DfTWP)
#TWP20t18 =  LTwp(DfTWP)
#TWP20t27 =  LTwp(DfTWP)
#TWP40t9 =   LTwp(DfTWP)
#TWP40t18 =  LTwp(DfTWP)
#TWP40t27 =  LTwp(DfTWP)

def Combine3(df1,df2,df3): 
    df4 = pd.DataFrame(L)
    df4.columns = ['StormwaterPipes']
    df4['9Velocity(m/s)'] = df1['Velocity(m/s)']
    df4['9Depth(m)'] = df1['Depth(m)']
    df4['9Discharge(m3/s)'] = df1['Discharge(m3/s)']
    df4['18Velocity(m/s)'] = df2['Velocity(m/s)']
    df4['18Depth(m)'] = df2['Depth(m)']
    df4['18Discharge(m3/s)'] = df2['Discharge(m3/s)']
    df4['27Velocity(m/s)'] = df3['Velocity(m/s)']
    df4['27Depth(m)'] = df3['Depth(m)']
    df4['27Discharge(m3/s)'] = df3['Discharge(m3/s)']
    
    return df4

Lsize10 = [20,50,80,100,10]
RainSl = [10,10,10,10,20,20,20,20,40,40,40,40]
RainSl1 = [10,10,10,10,10,20,20,20,20,20,40,40,40,40,40]
lac = [10,10]
l10 =[10,10,10,10]
l20 =[20,20,20,20]
l40 = [40,40,40,40]
l101 =[10,10,10,10,10]
l201 =[20,20,20,20,20]
l401 = [40,40,40,40,40]
def Combine3Twp(df1,df2,df3, li,ls):
    df4 = pd.DataFrame(li)
    df4.columns = ['Rain(mm)']
    df4['TWPsize'] = ls
    df4['9TWPhetro'] = df1['TWPhetro']
    df4['9HeteroTss(kg)'] =df1['HeteroTss(kg)']
    df4['9HeteroOrg(kg)'] = df1['HeteroOrg(kg)']
    df4['9TWPin'] = df1['TWPin']
    df4['9TWPout'] = df1['TWPout']
    df4['9TWPprist'] = df1['TWPprist']
    df4['9MassSettle(kg)'] = df1['MassSettle(kg)']
    df4['18TWPhetro'] = df2['TWPhetro']
    df4['18HeteroTss(kg)'] = df2['HeteroTss(kg)']
    df4['18HeteroOrg(kg)'] = df2['HeteroOrg(kg)']
    df4['18TWPin'] = df2['TWPin']
    df4['18TWPout'] = df2['TWPout']
    df4['18TWPprist'] = df2['TWPprist']
    df4['18MassSettle(kg)'] = df2['MassSettle(kg)']
    df4['27TWPhetro'] = df3['TWPhetro']
    df4['27HeteroTss(kg)'] = df3['HeteroTss(kg)']
    df4['27HeteroOrg(kg)'] = df3['HeteroOrg(kg)']
    df4['27TWPin'] =  df3['TWPin']
    df4['27TWPout'] = df3['TWPout']
    df4['27TWPprist'] = df3['TWPprist']
    df4['27MassSettle(kg)'] = df3['MassSettle(kg)']
    
    return df4

def Combine3TwpP(num,Rl,n,lis1,lis2,lis3,ls): 
    name1 = Combine3Twp(TWP10t9[num],TWP10t18[num],TWP10t27[num],lis1,ls) 
    name2 = Combine3Twp(TWP20t9[num], TWP20t18[num], TWP20t27[num],lis2,ls)   
    name3 = Combine3Twp(TWP40t9[num], TWP40t18[num], TWP40t27[num],lis3,ls)
    df7 = pd.DataFrame(Rl)
    df7.columns = ['Rain(mm)']
    df7['TWPsize'] = np.nan
    df7['9TWPhetro'] = np.nan
    df7['9HeteroTss(kg)'] = np.nan
    df7['9HeteroOrg(kg)'] = np.nan
    df7['9TWPin'] = np.nan
    df7['9TWPout'] = np.nan
    df7['9TWPprist'] = np.nan
    df7['9MassSettle(kg)'] = np.nan
    df7['18TWPhetro'] = np.nan
    df7['18HeteroTss(kg)'] = np.nan
    df7['18HeteroOrg(kg)'] = np.nan
    df7['18TWPin'] = np.nan
    df7['18TWPout'] = np.nan
    df7['18TWPprist'] = np.nan
    df7['18MassSettle(kg)'] = np.nan
    df7['27TWPhetro'] = np.nan
    df7['27HeteroTss(kg)'] = np.nan
    df7['27HeteroOrg(kg)'] = np.nan
    df7['27TWPin'] = np.nan
    df7['27TWPout'] = np.nan
    df7['27TWPprist'] = np.nan
    df7['27MassSettle(kg)'] = np.nan
    for i in range(0,n) : 
         df7.loc[i] = name1.loc[i].copy()
         df7.loc[i+n] = name2.loc[i].copy()
         df7.loc[i+ 2*n] = name3.loc[i].copy()
    
          
    return df7 
    

TWPvaRe = Combine3TwpP(0,RainSl,4,l10,l20,l40, Lsize)
TWPenRe = Combine3TwpP(1,RainSl,4,l10,l20,l40, Lsize)
TWPnaRe = Combine3TwpP(2,RainSl,4,l10,l20,l40,l10 )
TWPWacRe = Combine3TwpP(3,lac, 2,l10,l20,l40, l10)
TWPWbRe = Combine3TwpP(4,RainSl, 4,l10,l20,l40, Lsize)
TWPWdRe = Combine3TwpP(5,RainSl1,5,l101,l201,l401, Lsize10 )
TWPWlaRe = Combine3TwpP(6, RainSl1,5, l101,l201,l401,Lsize10)


Flp103 = Combine3(Flp10t9, Flp10t18,Flp10t27)
Flp203 = Combine3(Flp20t9,Flp20t18,Flp20t27)
Flp403 = Combine3(Flp20t9,Flp20t18,Flp20t27)
#dfR= [Flp10t9,Flp10t18,Flp10t27,Flp20t9,Flp20t18,Flp20t27,Flp40t9,Flp40t18,Flp40t27]

# provision made for depth and dishcarge( in mm and L/s)
def Reardf(df9,df18,df27,n): 
    redf = pd.DataFrame(L)
    redf.columns = ['StormwaterPipes']
    redf['15min'] = np.nan
    redf['30min'] = np.nan
    redf['45min'] = np.nan
    for i in range(len(L)):
        redf.iloc[i,1] = df9.iloc[i,n] *1000000
        redf.iloc[i,2] = df18.iloc[i,n] *1000000
        redf.iloc[i,3] = df27.iloc[i,n] *1000000
    #redf = redf.set_index(redf['StormwaterPipes'])
    #redf = redf.drop(columns = ['StormwaterPipes'])
    return redf


Redf10V = Reardf(Flp10t9,Flp10t18,Flp10t27,1)
Redf20V = Reardf(Flp20t9,Flp20t18,Flp20t27,1)
Redf40V = Reardf(Flp40t9,Flp40t18,Flp40t27,1)
Redf10D = Reardf(Flp10t9,Flp10t18,Flp10t27,2)
Redf20D = Reardf(Flp20t9,Flp20t18,Flp40t27,2)
Redf40D = Reardf(Flp40t9,Flp40t18,Flp40t27,2)
Redf10Q = Reardf(Flp10t9,Flp10t18,Flp10t27,3)
Redf20Q = Reardf(Flp20t9,Flp20t18,Flp20t27,3)
Redf40Q = Reardf(Flp40t9,Flp40t18,Flp40t27,3)
#TO excel funtion 

def ToEx(df,p): 
    df.to_excel(p)

ToEx(Flp103,'D:\Master thesis\Graphs\Results\ExcelR\Flp103.xlsx')
ToEx(Flp203,'D:\Master thesis\Graphs\Results\ExcelR\Flp203.xlsx')
ToEx(Flp403,'D:\Master thesis\Graphs\Results\ExcelR\Flp403.xlsx')

ToEx(TWPvaRe,'D:\Master thesis\Graphs\Results\ExcelR\TWPvaRe.xlsx')
ToEx(TWPenRe,'D:\Master thesis\Graphs\Results\ExcelR\TWPenRe.xlsx')
ToEx(TWPnaRe,'D:\Master thesis\Graphs\Results\ExcelR\TWPnaRe.xlsx')
ToEx(TWPWacRe,'D:\Master thesis\Graphs\Results\ExcelR\TWPWacRe.xlsx')
ToEx(TWPWbRe,'D:\Master thesis\Graphs\Results\ExcelR\TWPWbRe.xlsx')
ToEx(TWPWdRe,'D:\Master thesis\Graphs\Results\ExcelR\TWPWdRe.xlsx')
ToEx(TWPWlaRe,'D:\Master thesis\Graphs\Results\ExcelR\TWPWlaRe.xlsx')

ToEx(Redf10V,'D:\Master thesis\Graphs\Results\ExcelR\Redf10V.xlsx')
ToEx(Redf20V,'D:\Master thesis\Graphs\Results\ExcelR\Redf20V.xlsx')
ToEx(Redf40V,'D:\Master thesis\Graphs\Results\ExcelR\Redf40V.xlsx')
ToEx(Redf10D,'D:\Master thesis\Graphs\Results\ExcelR\Redf10D.xlsx')
ToEx(Redf20D,'D:\Master thesis\Graphs\Results\ExcelR\Redf20D.xlsx')
ToEx(Redf40D,'D:\Master thesis\Graphs\Results\ExcelR\Redf40D.xlsx')
ToEx(Redf10Q,'D:\Master thesis\Graphs\Results\ExcelR\Redf10Q.xlsx')
ToEx(Redf20Q,'D:\Master thesis\Graphs\Results\ExcelR\Redf20Q.xlsx')
ToEx(Redf40Q,'D:\Master thesis\Graphs\Results\ExcelR\Redf40Q.xlsx')








        



#Redf10V,Redf20V,Redf40V,Redf10D,Redf20D,Redf40D,Redf10Q,Redf20Q,Redf40Q
 
def Subpdf(df1,df2,df3,l):
    
    fig, (ax1,ax2,ax3) = plt.subplots(3,figsize=(12,5))
    ax1.scatter(df1.iloc[:,0], df1.iloc[:,1], color = 'Skyblue', label = '15mins', marker = 'o')
    ax1.scatter(df1.iloc[:,0], df1.iloc[:,2].values, color = 'Black', label = '30mins', marker = '^')
    ax1.scatter(df1.iloc[:,0], df1.iloc[:,3], color = 'r', label = '45mins', marker = 's')
    ax1.margins()
    ax1.set_xticks([])
    ax2.scatter(df2.iloc[:,0], df2.iloc[:,1], color = 'Skyblue', marker = 'o')
    ax2.scatter(df2.iloc[:,0], df2.iloc[:,2].values, color = 'Black', marker = '^')
    ax2.scatter(df2.iloc[:,0], df2.iloc[:,3], color = 'r', marker = 's')
    ax2.set_xticks([])
    ax2.set_ylabel(l)
    ax3.scatter(df3.iloc[:,0], df3.iloc[:,1], color = 'Skyblue', marker = 'o')
    ax3.scatter(df3.iloc[:,0], df3.iloc[:,2].values, color = 'Black', marker = '^')
    ax3.scatter(df3.iloc[:,0], df3.iloc[:,3], color = 'r', marker = 's')
    ax3.set_xlabel('Storm Water Pipe Name')
    fig.legend()
    
    
    
    
    
 
Subpdf(Redf10V,Redf20V,Redf40V,'Velocity(m/s)')    
Subpdf(Redf10D,Redf20D,Redf40D,'Depth(mm)') 
Subpdf(Redf10Q,Redf20Q,Redf40Q,'Discharge(L/s)')  
    
    
     

  
