# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def silnia(x):
    funkcja=np.vectorize(np.math.factorial, otypes=[float])
    return funkcja(x)

n=np.arange(0,20,1,dtype='float64')
n=np.tile(n.reshape(np.size(n),1),(1,3)).T
L=np.array([1,2,10],dtype='float64')
L=np.tile(L.reshape(np.size(L),1),(1,20))

#Rozkład Poissona losowa liczba towarów po cenie promocyjnej

P_promo= ((np.e**(-L))*(L**n))/silnia(n)

#Rys. 1. Rozkład Poissona dla różnych wartości oczekiwanych

fig, (ax1,ax2,ax3) = plt.subplots(1,3)

ax1.set_xticks(np.arange(0,21,4)) 
ax2.set_xticks(np.arange(0,21,4))
ax3.set_xticks(np.arange(0,21,4))

ax1.bar(n[0,:],P_promo[0,:],width=0.4,color='red')
ax2.bar(n[1,:],P_promo[1,:],width=0.4,color='green')
ax3.bar(n[2,:],P_promo[2,:],width=0.4,color='blue')
ax1.set_ylim(0,0.4)
ax2.set_ylim(0,0.4)
ax3.set_ylim(0,0.4)
ax1.legend(['L = 1'])
ax2.legend(['L = 2'])
ax3.legend(['L = 10'])
ax1.set_ylabel('P(n)')
ax2.set_ylabel('P(n)')
ax3.set_ylabel('P(n)')
ax1.set_xlabel('n')
ax2.set_xlabel('n')
ax3.set_xlabel('n')
fig.set_figwidth(10)
