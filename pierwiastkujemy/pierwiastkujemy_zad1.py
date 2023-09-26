# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

#pierwiastek kwadratowy dodatniej liczby a
def pierw(a):
    for i in range(0,1000000):
        if(i==0):
            xn=a
        else:
            poprz=xn
            xn = (xn + (a/xn))/2
            if ( xn-poprz==0 ):
                return i+1 #zwraca iteracje
                #return xn #zwraca pierwiastek
                
#pierwiastek kwadratowy dla tablicy odatnich liczb a 
def pierw_t(x):
    funkcja=np.vectorize(pierw)
    return funkcja(x)

c=np.linspace(-300,300,601)
m=np.random.rand(601,100)

cc=np.tile(c.reshape(np.size(c),1),(1,100))

liczby_a=m*10**cc

max_iteracje=np.max(pierw_t(liczby_a),1)
min_iteracje=np.min(pierw_t(liczby_a),1)

#wykres
f=plt.figure(1)
plt.plot(c,max_iteracje,'-',color='red')
plt.plot(c,min_iteracje,'-',color='blue')

plt.grid(True)
plt.xlabel('c')
plt.ylabel('max. i min. liczba iteracji dla danego c')
plt.legend(['max. liczba iteracji','min. liczba iteracji'])
plt.title('Wyniki symulacji')
f.set_figwidth(10)
f.set_figheight(10)