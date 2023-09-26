# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def blad(x):
    if (x<10**(-15)):
        return True
    else:
        return False

def pierw(m2,K):
    iteracje=np.full_like(m2,0)
    for i in range(len(m2)):
        for j in range(len(m2[0])):
            for k in range(0,10000):
                if(k==0):
                    x0=K[int(np.round( 10*m2[i,j] ) -10 )] #wartosc dla pierwszej iteracji
                    xn=(x0 + (1/(2*x0)) * (m2[i,j]-x0**2 ) )
                else:
                    poprz=xn
                    xn= (xn + (1/(2*x0)) * (m2[i,j]-xn**2 ) )  
                    if ( blad(abs(xn-poprz)) ):
                        iteracje[i,j]=k+1 #xn lub #k+1
                        break
    return iteracje

L=1000 #liczba losowanych m2 (1000)
C=13 # krok dla c2
c2=np.arange(-300,300,C,dtype='float64')
m2=np.random.uniform(low=1, high=10,size=(1,L) )  #losowanie 1000 wartosci m2
K=np.sqrt(np.linspace(1,9.9,100)) #wartosci w ROM
m2=np.tile(m2,(len(c2),1))
c2=np.tile(c2.reshape(np.size(c2),1),(1,L))

liczby_a=m2*10**c2 #liczby z ktorych liczony jest pierwiastek
srednie_iteracje=np.mean(pierw(m2,K),0)

#wykres
f=plt.figure(1)
plt.plot(m2[0,:],srednie_iteracje,'.',color='blue')

plt.grid(True)
plt.xlabel('m2')
plt.ylabel('Srednia liczba iteracji dla danego m2')
plt.legend(['srednia liczba iteracji dla danego m2'])
plt.title('Wyniki symulacji')