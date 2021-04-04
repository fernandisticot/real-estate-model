# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 20:06:44 2021

@author: fernandistico
"""

from math import *
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


##########################################################################

###Definir diccionario de zonas####
zones={}
for i in range(-3,4):
    for j in range(-3,4):
        zones[i,j]=(i,j)
####calcular numeo de zonas
num_de_zonas=0
for (i,j) in zones:
    num_de_zonas= num_de_zonas +1
    

####definir horizonte temporal
periodos={}
for t in range(20):
    periodos[t]=t
####definir tipos de activos
tipos={}
for v in range(3):
    tipos[v]=v
#####definir Svt, EXOGENO #########
svt={}
for v in tipos:
    for t in periodos:
        svt[v,t]=9800*(1+0.05*t)
        

###########costos de demolicion##############
cdvt={}
for t in periodos:
    cdvt[0, t]=0.00171
    cdvt[1, t]=0.00048
    cdvt[2, t]=0.00015

################costos de construcion######################
ccvt={}
for t in periodos:
    ccvt[0,t]= 0.00517
    ccvt[1,t]= 0.00455
    ccvt[2,t]= 0.0023
##tamaños de edificacion
qcv={}
qcv[0]=50
qcv[1]=125
qcv[2]=350

#####definir los precios de venta
pvit={}
for v in tipos:
    for (i,j) in zones:
        for t in periodos:
                pvit[v,(i,j),t]= 0.5+ 0.03*qcv[v] -0.5*sqrt(i**2 + j**2) + 0.1*t



######definir costos de renovacion
IRvt={}
for v in tipos:
    for t in periodos:
           IRvt[v,t]= 0.05+ 0.001*qcv[v]
        
#####Calcular los profit##
profitse_vit={}
for v in tipos:
    for (i,j) in zones:
        for t in periodos:
            if t==0 :
                profitse_vit[v,(i,j),t]=(pvit[v,(i,j),t] - IRvt[v,t])
            else:
                profitse_vit[v,(i,j),t]=pvit[v,(i,j),t-1]+ -IRvt[v,t]

# #############definir costos del desarrollador
            
# IDvit={}
# for v in tipos:
#     for (i,j) in zones:
#         for t in periodos:
#             if t==0 :
#                 IDvit[v,(i,j),t]= pvit[v,(i,j),t]/1.05*0.8
#             else:
#                 IDvit[v,(i,j),t]= pvit[v,(i,j),t-1]/1.035*0.8
                
# #########calcular profits del dsarrollador###
# profitsn_vit={}
# for v in tipos:
#     for (i,j) in zones:
#         for t in periodos:
#             profitsn_vit[v,(i,j),t]=pvit[v,(i,j),t]-IDvit[v,(i,j),t]

# ############calcular profit promedio de construir en i##################



########Profit wvit##################
profitwvit={}
for(i,j) in zones:
    for w in tipos:
        for v in tipos:    
            for t in periodos:
                   profitwvit[w,v,(i,j),t]= -pvit[w,(i,j),t] - cdvt[v,t]*qcv[w]- ccvt[v,t]*qcv[v] + pvit[v,(i,j),t]
##########Profit wit#################
profitwit={}
for(i,j) in zones:
    for w in tipos:
            for t in periodos:
                   profitwit[w,(i,j),t]= -1*pvit[w,(i,j),t] + -1*cdvt[w,t]*qcv[w]
##########Provit vit###################
profitvit={}
for(i,j) in zones:
        for v in tipos:    
            for t in periodos:
                   profitvit[v,(i,j),t]= -1* ccvt[v,t]*qcv[v] + pvit[v,(i,j),t]

#############IMPONER PROFITS Y PRECIOS MINIMOS############################
profitminse_vit={}
profitminde_vit={}
pminvit={}
for v in tipos:
    for (i,j) in zones:
        for t in periodos: 
        
            if t==0 or t==1 or t==2:
                
                pminvit[v,(i,j),t]= pvit[v,(i,j),t]
                
            else:
                pminvit[v,(i,j),t]= pvit[v,(i,j),t-1] + 0.75*(pvit[v,(i,j),t-1] - pvit[v,(i,j),t-2]) + 0.25*(pvit[v,(i,j),t-2] - pvit[v,(i,j),t-3])
                
            profitminde_vit[v,(i,j),t]= (pvit[v,(i,j),t] + cdvt[v,t]*qcv[v])*0.025 
            
            auxprofitseminzona=[]
            auxprofitsemintipo=[]
            profitminse_vit[v,(i,j),t]=0
            # for (a,b) in zones:
            #     auxprofitseminzona.append(pvit[v,(a,b),t])
            # auxprofitseminzona=sorted(auxprofitseminzona)
            # for w in tipos:
            #     auxprofitsemintipo.append(pvit[w,(i,j),t])
            # auxprofitsemintipo=sorted(auxprofitsemintipo)    
            # auxprofitsemin.append(auxprofitseminzona[0])
            # auxprofitsemin.append(auxprofitsemintipo[0])
            # auxprofitsemin.sort()
            # profitminse_vit[v,(i,j),t]=auxprofitsemin[1]
        
            

############calcular probabilidades##########
theta=[]
ni=[]
# eta=[]
# lamda=[]
otrolamda=[]
for t in periodos:
    auxprofitse=[]
    auxpvit=[]
    # auxprofitsn=[]
    auxprofitpwvit=[]
    for v in tipos:
        for (i,j) in zones:
           auxprofitse.append(round(pi/(sqrt(6)*0.1*abs(profitse_vit[v,(i,j),t])),3))
           auxpvit.append(round(pi/(sqrt(6)*0.1*abs(pvit[v,(i,j),t])),3))
           # auxprofitsn.append(round(pi/(sqrt(6)*0.1*abs(profitsn_vit[v,(i,j),t])),3))
           for w in tipos:
                   auxprofitpwvit.append(round(pi/sqrt(6)*0.1*abs((profitwvit[w,v,(i,j),t])),3))
    theta.append(sum(auxprofitse)/(len(tipos)*len(zones)))     
    ni.append(sum(auxpvit)/(len(tipos)*len(zones)))
    # lamda.append(sum(auxprofitsn)/(len(tipos)*len(zones)))
    otrolamda.append(sum(auxprofitpwvit)/(len(tipos)*len(tipos)*len(zones)))


    
logsumaprofitvit={}
for (i,j) in zones:
    for t in periodos:
        aux=[]
        for v in tipos:
            aux.append(exp(otrolamda[t]*profitvit[v,(i,j),t]))
        logsumaprofitvit[(i,j),t]= (1/otrolamda[t])*log(sum(aux))
            
logsumaprofitwit={}
for (i,j) in zones:
    for t in periodos:
        aux=[]
        for v in tipos:
            aux.append(exp(otrolamda[t]*profitwit[v,(i,j),t]))
        logsumaprofitwit[(i,j),t]= (1/otrolamda[t])*log(sum(aux))

P_Evit={}
P_Svit={}
P_Nvit={}
P_WVit={}
P_Wit={}
P_Vit={}


for v in tipos:
    for (i,j) in zones:
        for t in periodos:
            P_Evit[v,(i,j),t]=(exp(theta[t]*(profitse_vit[v,(i,j),t]-profitminse_vit[v,(i,j),t]))/
                (exp(theta[t]*(profitse_vit[v,(i,j),t]-profitminse_vit[v,(i,j),t]))+1))
                
            P_Svit[v,(i,j),t]=(exp(ni[t]*(pvit[v,(i,j),t]-pminvit[v,(i,j),t]))/
                (exp(ni[t]*(pvit[v,(i,j),t]-pminvit[v,(i,j),t]))+1))

denominadorpwit=[]
for t in periodos:
    auxdenominadorpwit=[]
    for w in tipos:
        for (i,j) in zones:
            auxdenominadorpwit.append(exp(otrolamda[t]*(profitwit[w,(i,j),t] + logsumaprofitvit[(i,j),t])))
    denominadorpwit.append(sum(auxdenominadorpwit))

for t in periodos:
    for w in tipos:
        for (i,j) in zones:
            P_Wit[w,(i,j),t]=(exp(otrolamda[t]*(profitwit[w,(i,j),t] + logsumaprofitvit[(i,j),t]))/
                   denominadorpwit[t])
            
denominadorpvit={}

for t in periodos:
    for v in tipos:
        auxdenominadorpvit=[]
        for (i,j) in zones:
            auxdenominadorpvit.append(exp(otrolamda[t]*(profitvit[v,(i,j),t] + logsumaprofitwit[(i,j),t])))
        denominadorpvit[v,t]=sum(auxdenominadorpvit)

for t in periodos:
    for (i,j) in zones:
        for v in tipos:
            P_Vit[v,(i,j),t]=(exp(otrolamda[t]*(profitvit[v,(i,j),t] + logsumaprofitwit[(i,j),t]))/
                   denominadorpvit[v,t])                                   
                            

##############################################################################
########***********####### REALIZAR SIMULACION ########***********############
##############################################################################
Svit={}
MEvit={}
OEvit={}
OEt={}
Dvit={}
Dvt={}
Nvt={}
Nvit={}
ONvit={}

for v in tipos:
    for (i,j) in zones:
        Svit[v,(i,j),0]=200

t=1
while t<=len(periodos)-1:
    
    auxvendido=[]
    for(i,j) in zones:
        for w in tipos:          
            MEvit[w,(i,j),t]=Svit[w,(i,j),t-1]*P_Evit[w,(i,j),t]
            OEvit[w,(i,j),t]=MEvit[w,(i,j),t]*P_Svit[w,(i,j),t]
            auxvendido.append(OEvit[w,(i,j),t])
    OEt[t]=sum(auxvendido)        
    
    for w in tipos:
        auxdemolido=[]
        for (i,j) in zones:
            Dvit[w,(i,j),t]=OEt[t]*P_Wit[w,(i,j),t]
            auxdemolido.append(Dvit[w,(i,j),t])
        Dvt[w,t]=sum(auxdemolido)
        Nvt[w,t]=Dvt[w,t]+svt[w,t]-svt[w,t-1]
    
    for(i,j) in zones:    
        for v in tipos:
            Nvit[v,(i,j),t]=(Nvt[v,t])*P_Vit[v,(i,j),t]
            ONvit[v,(i,j),t]=Nvit[v,(i,j),t]*P_Svit[v,(i,j),t]  
            Svit[v,(i,j),t]=Svit[v,(i,j),t-1] - Dvit[v,(i,j),t]+Nvit[v,(i,j),t]   
    t+=1 

##############################################################################
#######********####### FIN DE SIMULACION #############*******#################
##############################################################################

#########Crear series de tiempo##########################

#Precios, renovación y profits de entrar al mercado

# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
#         auxe=[]
#         auxf=[]
#         auxg=[]
#         for t in range(1,len(periodos)):
#             auxd.append(IRvt[v,t])
#             auxe.append(profitse_vit[v,(i,j),t])
#             auxf.append(pvit[v,(i,j),t])
#             auxg.append(profitminse_vit[v,(i,j),t])
#         plt.figure()
#         plt.ylim(bottom=0,top=12)
#         plt.xlim(left=0,right=18)
#         plt.grid(color='k', linestyle='-', linewidth=0.1)
#         plt.plot(range(len(auxd)),auxd,label='IRvt',color='r')
#         plt.plot(range(len(auxe)),auxe,label='Profit',color='b')
#         plt.plot(range(len(auxf)),auxf,label='Pvit', color='g')
#         plt.plot(range(len(auxg)),auxg,label='ProfitMin',color='k')
#         plt.title( ' Precios de venta, costos de renovación y profit. v='
#                   +str(v+1)+' i='+str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('profitse,profitmin, precio y renovacion'+str(v+1)+str((i,j)))
#         plt.show()
#         plt.close(fig=None)
#         v=v+1


# # #Probabilidades salir al mercado
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
       
#         for t in range(1,len(periodos)):
#             auxd.append(P_Evit[v,(i,j),t])         
#         plt.figure()
#         plt.plot(range(len(auxd)),auxd,label='tipo'+str(v),color='b')
#         plt.ylim(top=1, bottom=0)
#         plt.xlim(left=0,right=18)
#         plt.title( 'PEvit, v='+str(v+1) + ' i='+str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('Pob E vit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1


# # cantidades en el mercado
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
#         auxe=[]
       
#         for t in range(1,len(periodos)):
#             auxd.append(MEvit[v,(i,j),t])
#             auxe.append(Svit[v,(i,j),t-1])
          
#         plt.figure()
#         plt.ylim(bottom=0,top=1000)
#         plt.xlim(left=0,right=18)
#         plt.plot(range(len(auxd)),auxd,label='MEvit, v='+str(v)+ ' i=' +str((i,j)),color='b')
#         plt.plot(range(len(auxe)),auxe,label='Svi(t-1)') 
#         plt.title( 'MEvit ^ Svit , v='+str(v+1)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('MEvit ^ Svit , v='+str(v)+ ', i=' +str((i,j)))
#         plt.close(fig=None)
#         v=v+1





# relacion precios precios minimos  de venta

# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
#         auxe=[]
#         for t in range(1,len(periodos)):
#             auxd.append(pvit[v,(i,j),t])
#             auxe.append(pminvit[v,(i,j),t])
#         plt.figure()
#         plt.ylim(top=18,bottom=0)
#         plt.xlim(left=0,right=18)
#         plt.plot(range(len(auxd)),auxd,label='precio')
#         plt.plot(range(len(auxe)),auxe ,label='pmin')
#         plt.title('pvit, i='+str((i,j)) + ' v='+str(v+1))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('precios'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1





#Probabilidades de ser ventido  PS
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]  
#         for t in range(1,len(periodos)):
#             auxd.append(P_Svit[v,(i,j),t]) 
#         plt.figure()
#         plt.ylim(bottom=0,top=1)
#         plt.xlim(left=0,right=18)
#         plt.plot(range(len(auxd)),auxd,label='tipo'+str(v),color='b')
#         plt.title( 'PSvit, v='+str(v+1)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('Pob s vit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1



# # cantidades vendidas
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
#         auxe=[]
#         auxf=[]
#         for t in range(1,len(periodos)):
#             auxd.append(OEvit[v,(i,j),t])
#             auxe.append(MEvit[v,(i,j),t])
#             auxf.append(Svit[v,(i,j),t])
#         plt.figure()
#         plt.ylim(bottom=0,top=1000)
#         plt.xlim(left=0,right=18)
#         plt.plot(range(len(auxd)),auxd,label='OEvit',color='b')
#         plt.plot(range(len(auxe)),auxe,label='MEvit')
#         plt.plot(range(len(auxf)),auxf,label='Svit')
#         plt.title( 'OEvit, v='+str(v+1)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('OEvit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1






#Profits de demoliciones


# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
#         auxe=[]
#         auxf=[]
#         auxg=[]
#         for t in range(1,len(periodos)):
#             auxd.append(logsumaprofitvit[(i,j),t])
#             auxe.append(profitwit[v,(i,j),t])
#             auxf.append(cdvt[v,t]*qcv[v])
#             auxg.append(pvit[v,(i,j),t])
#         plt.figure()
#         plt.ylim(bottom=-18,top=18)
#         plt.xlim(left=0,right=18)
#         plt.plot(range(len(auxd)),auxd,label='E(max profit vit)'+str(v),color='b')
#         plt.plot(range(len(auxe)),auxe,color='r',label='Profit wit')
#         plt.plot(range(len(auxf)),auxf,label='cdvitqcwit',color='g')
#         plt.plot(range(len(auxg)),auxg,label='Precio wit',color='k')
#         plt.title( 'Demolición v='+str(v+1)+' i='+str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('profit dmeolicion  profit min'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1











# # #Probabilidades de ser demolido
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
       
#         for t in range(1,len(periodos)):
#             auxd.append(P_Wit[v,(i,j),t])
          
#         plt.figure()
#         plt.xlim(left=0,right=18)
#         plt.ylim(bottom=0,top=0.02)
#         plt.plot(range(len(auxd)),auxd,label='tipo'+str(v),color='b')
#         plt.title( 'P_Wit, w='+str(v+1)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('Pob D vit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1




# # cantidades demolidas
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
#         auxe=[]
#         auxf=[]
#         auxg=[]
#         for t in range(1,len(periodos)):
#             auxd.append(OEvit[v,(i,j),t])
#             auxe.append(MEvit[v,(i,j),t])
#             auxf.append(Svit[v,(i,j),t])
#             auxg.append(Dvit[v,(i,j),t])
#         plt.figure()
#         plt.ylim(bottom=0,top=600)
#         plt.xlim(left=0,right=18)
#         plt.plot(range(len(auxd)),auxd,label='OEvit',color='b')
#         plt.plot(range(len(auxe)),auxe,label='MEvit')
#         plt.plot(range(len(auxf)),auxf,label='Svit')
#         plt.plot(range(len(auxg)),auxg,label='Dvit')
#         plt.title( 'Dvit, v='+str(v+1)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('Dvit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1







##Demolido
    
  
# auxe=[]
# auxf=[]
# auxg=[]
# auxh=[]
# for t in range(1,len(periodos)):
#         auxe.append(svt[0,t])
#         auxf.append(Dvt[0,t])
#         auxg.append(Dvt[1,t])
#         auxh.append(Dvt[2,t])
# plt.figure()
# plt.plot(range(len(auxe)),auxe,label='Svt v={1,2,3}', color='b')
# plt.plot(range(len(auxe)),auxf,label='D1t', color='g')
# plt.plot(range(len(auxe)),auxg,label='D2t', color='y')
# plt.plot(range(len(auxf)),auxh,label='D3t',color='r')
# plt.title('Dvt Svt, v'  )
# plt.legend(loc=2,ncol=2)
# plt.savefig('Dvt')

         
# nuevo total
    
    # v=0
    # while v<=2:  
    #     auxd=[]
    #     auxe=[]

    #     for t in range(1,len(periodos)):
    #         auxd.append(Nvt[v,t])
    #         auxe.append(Dvt[v,t])
    #     plt.figure()
    #     plt.ylim(bottom=0,top=30000)
    #     plt.xlim(left=0,right=18)
    #     plt.plot(range(len(auxd)),auxd,label='Nvt, v='+str(v+1), color='b')
    #     plt.plot(range(len(auxe)),auxe,label='Dvt, v='+str(v+1),color='r')
    #     plt.title('Nvt Dvt')
    #     plt.legend(loc=2,ncol=2)
    #     plt.savefig('Nuevos activos total'+str(v))
    #     plt.close(fig=None)
    #     v=v+1  



# # Nuevos activos
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]       
#         for t in range(1,len(periodos)):
#             auxd.append(Nvit[v,(i,j),t])          
#         plt.figure()
#         plt.ylim(top=1000,bottom=0)
#         plt.xlim(0,18)
#         plt.plot(range(len(auxd)),auxd,label='tipo'+str(v),color='b')    
#         plt.title( 'Nvit, v='+str(v)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('Nvit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1




# #Nuevovendido
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
#         auxe=[]
#         for t in range(1,len(periodos)):
#             auxd.append(ONvit[v,(i,j),t])
#             auxe.append(Nvit[v,(i,j),t])
          
#         plt.figure()
#         plt.ylim(top=500, bottom=0)
#         plt.plot(range(len(auxd)),auxe,label='Nvit',color='b')
#         plt.plot(range(len(auxe)),auxd,label='ONvit',color='g')
#         plt.title( 'ONvit, v='+str(v)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('ONvit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1











# SVIT
# for (i,j) in zones:
#     v=0
#     while v<=2:  
#         auxd=[]
       
#         for t in range(1,len(periodos)):
#             auxd.append(Svit[v,(i,j),t])
          
#         plt.figure()
#         plt.plot(range(len(auxd)),auxd,label='tipo'+str(v),color='b')
        
#         plt.title( 'Svit, v='+str(v)+ ', i=' +str((i,j)))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig('Svit'+str(v)+str((i,j)))
#         plt.close(fig=None)
#         v=v+1





            
########################################################
########## Crear mapas de calor ##########################
########################################################

# # Pobabilities of opening for sale
# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         matriz=[]
#         for j in reversed(range(-3,4)):
#             otroaux=[]
#             for i in range(-3,4):
#                 otroaux.append(P_Evit[v,(i,j),t])
#             matriz.append(otroaux)
#         df=pd.DataFrame(matriz, index=list(range(-3,4)),columns=list(range(-3,4)))
#         plt.figure()
#         sns.heatmap(df, annot=True,vmin=0,vmax=1)
#         plt.title(label= 'PEvit ,' 'v=' +str(v+1) + 't=' + str(t))
#         plt.savefig('PEvit'+str(v)+'slash'+str(t))
#         plt.close(fig=None)
#         t=t+1
#     v=v+1

####probabilidad de ser efectivamente vendido PSvit

# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         matriz=[]
#         for j in reversed(range(-3,4)):
#             otroaux=[]
#             for i in range(-3,4):
#                 otroaux.append(P_Svit[v,(i,j),t])
#             matriz.append(otroaux)
#         df=pd.DataFrame(matriz, index=list(range(-3,4)),columns=list(range(-3,4)))
#         plt.figure()
#         sns.heatmap(df, annot=True, vmin=0, vmax=1)
#         plt.title(label='PSvit v='+str(v+1)+' t='+str(t))
#         plt.savefig('PSvit'+str(v)+'slash'+str(t))
#         plt.close(fig=None)
#         t=t+1
#     v=v+1
    
# plt.close('all')

# Probabiliad de ser DEMOLIDO

# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         matriz=[]
#         for j in reversed(range(-3,4)):
#             otroaux=[]
#             for i in range(-3,4):
#                 otroaux.append(P_Wit[v,(i,j),t])
#             matriz.append(otroaux)
#         df=pd.DataFrame(matriz, index=list(range(-3,4)),columns=list(range(-3,4)))
#         plt.figure()
#         sns.heatmap(df, annot=True, vmin=0,vmax=1)
#         plt.title(label='PWit v='+str(v+1)+' t='+str(t))
#         plt.savefig('PDvit'+str(v)+'  '+str(t))
#         plt.close(fig=None)
#         t=t+1
#     v=v+1




# ##Probabilidad de ser construido 

# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         matriz=[]
#         for j in reversed(range(-3,4)):
#             otroaux=[]
#             for i in range(-3,4):
#                 otroaux.append(P_Vit[v,(i,j),t])
#             matriz.append(otroaux)
#         df=pd.DataFrame(matriz, index=list(range(-3,4)),columns=list(range(-3,4)))
#         plt.figure()
#         sns.heatmap(df, annot=True, vmin=0,vmax=1)
#         plt.title(label='PVit v='+str(v+1)+' t='+str(t))
#         plt.savefig('PVit'+str(v)+'  '+str(t))
#         plt.close(fig=None)
#         t=t+1
#     v=v+1



# ###Nvit
# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         matriz=[]
#         for j in reversed(range(-3,4)):
#             otroaux=[]
#             for i in range(-3,4):
#                 otroaux.append(Nvit[v,(i,j),t])
#             matriz.append(otroaux)
#         df=pd.DataFrame(matriz, index=list(range(-3,4)),columns=list(range(-3,4)))
#         plt.figure()
#         sns.heatmap(df, annot=True,vmin=10,vmax=440)
#         plt.title(label='Nvit v='+str(v+1)+' t='+str(t))
#         plt.savefig('nvit'+str(v)+'  '+str(t))
#         plt.close(fig=None)
#         t=t+1
#     v=v+1
    
# # plt.close('all')    








# #Svit
# v=0
# while v<=2:
#     t=0
#     while t<=len(periodos)-1:
#         matriz=[]
#         for j in reversed(range(-3,4)):
#             otroaux=[]
#             for i in range(-3,4):
#                 otroaux.append(Svit[v,(i,j),t])
#             matriz.append(otroaux)
#         df=pd.DataFrame(matriz, index=list(range(-3,4)),columns=list(range(-3,4)))
#         plt.figure()
#         sns.heatmap(df, annot=True,vmin=0,vmax=500)
#         plt.title(label='Existing assets Svit, v='+str(v+1)+' t='+str(t))
#         plt.savefig( 'Svit' + str(v)+' ' +str(t))
#         plt.close(fig=None)
#         t=t+1
#     v=v+1
    
    
# ###PROFIT WVIT

# for w in tipos:
#     v=0
#     while v<=2:
#         t=0
#         while t<=len(periodos)-1:
#             matriz=[]
#             for j in reversed(range(-3,4)):
#                 otroaux=[]
#                 for i in range(-3,4):
#                     otroaux.append(profitwvit[w,v,(i,j),t])
#                 matriz.append(otroaux)
#             df=pd.DataFrame(matriz, index=list(range(-3,4)),columns=list(range(-3,4)))
#             plt.figure()
#             sns.heatmap(df, annot=True,vmin=-3.8,vmax=3.8)
#             plt.title(label='profit wvit, w='+str(w+1)+' v='+str(v+1) +' t='+str(t))
#             plt.savefig( 'profit wvit' +str(w) + ' ' + str(v)+' ' +str(t))
#             plt.close(fig=None)
#             t=t+1
#         v=v+1
    
    
    







##########################################################################
###############Gráficos de barra      ####################################
##########################################################################

#Precios ve tenta, costos de renovación, profits y profits minimos

# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         distancia=[]
#         preciosventa=[]
#         profitventa=[]
#         profitminimo=[]
#         inversionrenovacion=[]
#         for i in range(4):
#             for j in range(i+1):
#                 distancia.append((i,j))
#                 preciosventa.append(pvit[v,(i,j),t])
#                 inversionrenovacion.append(IRvt[v,t])
#                 profitventa.append(profitse_vit[v,(i,j),t])
#                 profitminimo.append(profitminse_vit[v,(i,j),t])
#         barWidth=0.1
#         r1 = np.arange(len(distancia))
#         r2 = [x + barWidth for x in r1]
#         r3 = [x + barWidth for x in r2]
#         r4 = [x + barWidth for x in r3]
#         plt.figure()
#         plt.ylim(bottom=0,top=15)
#         plt.bar(r1, preciosventa, color='r', width=barWidth, edgecolor='white', label='Pvit')
#         plt.bar(r2, inversionrenovacion, color='g', width=barWidth, edgecolor='white', label='IRvt')
#         plt.bar(r3, profitventa, color='b', width=barWidth, edgecolor='white', label='Profit')
#         plt.bar(r4, profitminimo, color='k', width=barWidth, edgecolor='white', label='Profit min')
#         plt.xlabel('(i,j)', fontweight='bold')
#         plt.xticks([r + barWidth for r in range(len(distancia))], distancia)
#         plt.legend(loc=2,ncol=2)
#         plt.title(label='v='+str(v+1))
#         plt.savefig('v='+str(v) +str(t))
#         plt.show()
#         t=t+1
#     v=v+1
# plt.close('all')





# #MEvit ,OEvit, Dvit , svit, Nvit, Onvit
# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         distancia=[]
#         m=[]
#         o=[]
#         d=[]
#         n=[]
#         on=[]
#         s=[]
#         for i in range(4):
#             for j in range(i+1):
#                 distancia.append((i,j))
#                 m.append(MEvit[v,(i,j),t])
#                 o.append(OEvit[v,(i,j),t])
#                 d.append(Dvit[v,(i,j),t])
#                 n.append(Nvit[v,(i,j),t])
#                 on.append(ONvit[v,(i,j),t])
#                 s.append(Svit[v,(i,j),t])
#         barWidth=0.1
#         r1 = np.arange(len(distancia))
#         r2 = [x + barWidth for x in r1]
#         r3 = [x + barWidth for x in r2]
#         r4 = [x + barWidth for x in r3]
#         r5 = [x + barWidth for x in r4]
#         r6 = [x + barWidth for x in r5]
#         r7 = [x + barWidth for x in r6]
#         plt.figure()



#         plt.ylim(bottom=0,top=700)
#         plt.bar(r1, m, color='#7f6d5f', width=barWidth, edgecolor='white', label='MEvit')
#         plt.bar(r2, o, color='#557f2d', width=barWidth, edgecolor='white', label='OEvit')
#         plt.bar(r3, d, color='#2d7f5e', width=barWidth, edgecolor='white', label='Dvit')
#         plt.bar(r4, n, color='r', width=barWidth, edgecolor='white', label='Nvit')
#         plt.bar(r5, on, color='b', width=barWidth, edgecolor='white', label='ONvit')
#         plt.bar(r6, s, color='k', width=barWidth, edgecolor='white', label='Svit')
#         plt.xlabel('(i,j)', fontweight='bold')
#         plt.xticks([r + barWidth for r in range(len(distancia))], distancia)
#         plt.title('v='+str(v+1)+ ' t='+str(t))
#         plt.legend(loc=2,ncol=2)
#         plt.savefig(str(v) + '  '+str(t))
#         plt.show()
#         t=t+1
#     v=v+1
# plt.close('all')
                



# # costos demolicion, profit snit, profitde, profit minimo 

# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         distancia=[]
#         profiwit=[]
#         esperanzaprofitvit=[]
#         costodemolicion=[]
#         preciowit=[]
#         for i in range(4):
#             for j in range(i+1):
#                 distancia.append((i,j))
#                 profiwit.append(-1*profitwit[v,(i,j),t])
#                 costodemolicion.append(cdvt[v,t]*qcv[v])
#                 esperanzaprofitvit.append(logsumaprofitvit[(i,j),t])
#                 preciowit.append(pvit[v,(i,j),t])
#         barWidth=0.1
#         r1 = np.arange(len(distancia))
#         r2 = [x + barWidth for x in r1]
#         r3 = [x + barWidth for x in r2]
#         r4 = [x + barWidth for x in r3]
#         plt.figure()
#         plt.ylim(bottom=-1,top=20)
#         plt.bar(r1, profiwit, color='k', width=barWidth, edgecolor='white', label='(-1)*Profit wit')
#         plt.bar(r2, esperanzaprofitvit, color='#557f2d', width=barWidth, edgecolor='white', label='E(profit vit)')
#         plt.bar(r3, costodemolicion, color='#2d7f5e', width=barWidth, edgecolor='white', label='cdvitqcv')
#         plt.bar(r4, preciowit, color='r', width=barWidth, edgecolor='white', label='pwit')
#         plt.xlabel('(i,j)', fontweight='bold')
#         plt.xticks([r + barWidth for r in range(len(distancia))], distancia)
#         plt.legend(loc=2,ncol=2)
#         plt.title(label='v='+str(v+1)+ ' t='+str(t))
#         plt.savefig('v='+str(v)+' ' +str(t))
#         plt.show()
#         t=t+1
#     v=v+1
# plt.close('all')





# Localizacion

# v=0
# while v<=2:
#     t=1
#     while t<=len(periodos)-1:
#         distancia=[]
#         profivit=[]
#         esperanzaprofitwit=[]
#         costoconstruccion=[]
#         preciovit=[]
#         for i in range(4):
#             for j in range(i+1):
#                 distancia.append((i,j))
#                 profivit.append(profitvit[v,(i,j),t])
#                 costoconstruccion.append(ccvt[v,t]*qcv[v])
#                 esperanzaprofitwit.append(-1*logsumaprofitwit[(i,j),t])
#                 preciovit.append(pvit[v,(i,j),t])
#         barWidth=0.1
#         r1 = np.arange(len(distancia))
#         r2 = [x + barWidth for x in r1]
#         r3 = [x + barWidth for x in r2]
#         r4 = [x + barWidth for x in r3]
#         plt.figure()
#         plt.ylim(bottom=-0.5,top=18)
#         plt.bar(r1, profivit, color='k', width=barWidth, edgecolor='white', label='Profit vit')
#         plt.bar(r2, esperanzaprofitwit, color='#557f2d', width=barWidth, edgecolor='white', label='(-1*)E(max (profit wit))')
#         plt.bar(r3, costoconstruccion, color='#2d7f5e', width=barWidth, edgecolor='white', label='ccvtqcv')
#         plt.bar(r4, preciovit, color='r', width=barWidth, edgecolor='white', label='pvit')
#         plt.xlabel('(i,j)', fontweight='bold')
#         plt.xticks([r + barWidth for r in range(len(distancia))], distancia)
#         plt.legend(loc=2,ncol=2)
#         plt.title(label='v='+str(v)+ ' t='+str(t))
#         plt.savefig('v='+str(v)+' ' +str(t))
#         plt.show()
#         t=t+1
#     v=v+1
# plt.close('all')

