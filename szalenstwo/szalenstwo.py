# -*- coding: utf-8 -*-

import scipy.special as sc
import numpy as np

def warun0(x0,ufn):
    if x0>=ufn:
        return True #mozna kontynuowac
    else: 
        return False
    
def warun(xt,xp,ufn):
    if xt<=ufn and xp>=ufn:
        return True #wtedy xp jest wynikiem
    else: 
        return False

def przedz_m(n,ufn):
    suma=0
    k=0
    suma+=sc.comb(n,k)/(2**n) 
    poprz=1-2*suma
    k+=1
    if warun0(1-2*suma,ufn)==False:
        return '-'
    while (k<n/2):
        suma+=sc.comb(n,k)/(2**n)
        if warun(1-2*suma,poprz,ufn):
            return k
        poprz=1-2*suma
        k+=1
    return '-'

def przedz_p(n,ufn,p):
    suma=0
    k=0
    suma+=sc.comb(n,k)*p**k*(1-p)**(n-k) 
    poprz=1-suma
    k+=1
    if warun0(1-suma,ufn)==False:
        return '-'
    while (k<n/2):
        suma+=sc.comb(n,k)*p**k*(1-p)**(n-k)
        if warun(1-suma,poprz,ufn):
            return k
        poprz=1-suma
        k+=1
    return '-'

#P10, C = 80% oraz C = 97%
p=0.10  #Pp
p1=0.80   #ufn
p2=0.97   #ufn
n=np.linspace(1,100,100)
tabela1=[]
for n in range (1,len(n)+1): #dla kazdego n
    tabela1.append( [ przedz_m(n,p1) , przedz_m(n,p2) , przedz_p(n,p1,p) , przedz_p(n,p2,p) ] )   
tabela1=np.array(tabela1)

'''
# tabela 1 - oryginalna TEST# 
p=0.1587  #Pp
p1=0.75   #ufn
p2=0.95   #ufn
n=np.linspace(1,100,100)
tabela1=[]
for n in range (1,len(n)+1): #dla kazdego n
    tabela1.append( [ przedz_m(n,p1) , przedz_m(n,p2) , przedz_p(n,p1,p) , przedz_p(n,p2,p) ] )   
tabela1=np.array(tabela1)
# tabela 1 - oryginalna TEST# 
'''
