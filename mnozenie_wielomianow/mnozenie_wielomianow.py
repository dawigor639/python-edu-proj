# -*- coding: utf-8 -*-

import time
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import least_squares

### Klasa ###
class Wielomian(list):
    
    def __init__(self, a=None):
        if (a is None):
           a = [] 
        #skracanie dlugosci listy
        while (a[-1] == 0):
            if(len(a) == 1):
                break
            a.pop()
        super().__init__(a)

    def __add__(self, b):
        a,b = self.zero(b)
        return Wielomian( (np.array(a) + np.array(b)) )
    
    def __sub__(self, b):
        a,b = self.zero(b) 
        roznica=(np.array(a) - np.array(b))
        return Wielomian( roznica )

    def zero(self, b):
        a = list(self)
        b = list(b)
        dlugosc = max(len(a), len(b))
        a = a + [0] * (dlugosc - len(a))
        b = b + [0] * (dlugosc - len(b))
        return (a,b)

    def __mul__(self,b):
            
            max_k = len(self) + len(b) - 2 # max_k = n + m 
            k = 1
            while (max_k >= 2**k):
                k += 1
            max_k = 2**k #najmniejsza liczba w postaci 2^k
            a = list(self)
            b = list(b)
            a = a + ([0] * (max_k-len(a)) ) #dlugosci a 
            b = b + ([0] * (max_k-len(b)) ) #dlugosci b
            a_fft=np.fft.fft(a)
            b_fft=np.fft.fft(b)
            return Wielomian ( np.round( np.real( np.fft.ifft(a_fft*b_fft)) , 13).tolist() )

def znaki(n):
    lista=[]
    for i in range(0,n):
        lista.append( random.choice([-1, 1]) )
    return lista
  
#parametry  
mini=0.
maks=0.1
N=10 #polowa liczby wielomianow
stopnie=np.linspace(100,1000,10).tolist() #stopnie wielomianow
stopnie= [int(i) for i in stopnie]

#rozklad Benforda
liczby_benford = np.linspace(1,9,9)
benford_prawd = np.log10(1 + 1/liczby_benford)  

#tworzenie 20 wielomianów stopnia od 100 do 1000 o watosciach 0.1 < abs(x) < 1
wielomiany = []
for i in range(0,N):
    #pierwszy wielomian
    znaczace = np.random.choice(liczby_benford, p=benford_prawd, size=stopnie[i]+1)/10 #generowanie cyfr znaczacych
    pozostale=np.random.uniform(mini,maks, size=( stopnie[i]+1 )) #generowanie 14-stu pozostalych cyfr
    wartosci=znaczace+pozostale
    znak=znaki(stopnie[i]+1)
    wielomiany.append( Wielomian(( ( wartosci*np.array(znak) ).tolist() ) ) )

for j in range(0,N):
    #drugi wielomian
    znaczace = np.random.choice(liczby_benford, p=benford_prawd, size=stopnie[j]+1)/10 #generowanie cyfr znaczacych
    pozostale=np.random.uniform(mini,maks, size=( stopnie[j]+1 )) #generowanie 14-stu pozostalych cyfr
    wartosci=znaczace+pozostale
    znak=znaki(stopnie[j]+1)
    wielomiany.append( Wielomian(( ( wartosci*np.array(znak) ).tolist() ) ) )        

#pomiar mnozenia 10 wielomianow * 10 wielomianow o takich samych stopniach       
pomiary_t=np.zeros(10).tolist()
Ti=0 #czas sortowania dla i-tej listy 
powtorzenia=np.zeros(10,dtype=int).tolist()
for i in range(0,N):
    
    while( pomiary_t[i]<3 ):
        powtorzenia[i]+=1
        start_Ti = time.time() #pomiar czasu start
        wielomiany[i]*wielomiany[i+N]
        koniec_Ti = time.time() #pomiar czasu stop
        Ti = koniec_Ti - start_Ti
        pomiary_t[i]+=Ti
    print('wykonano mnozenie nr:',i+1, 'w czasie:',pomiary_t[i],' s','powtorzenia:',powtorzenia[i])
    
pomiary_t_srednie =  np.array(pomiary_t) / np.array(powtorzenia)

#Wzor na czas 
def Model_T(a, b):
    T = (np.array(stopnie)**a) * (np.log2(np.array(stopnie))**b)
    return T

#Roznica miedzy czasem otrzymanym na podstawie wzoru i czasem z eksperymentu
def func1(x):
    # roznica
    return Model_T(x[0], x[1]) - pomiary_t_srednie

x0=[1,1] #przypuszcalne wartosci
res_1 = least_squares(func1, x0) #minimalizacja odleglosci sredniokwadratowej
czas_model=Model_T(res_1.x[0],res_1.x[1]) #czasu z modelu na podstawie wyznaczonych a i b

#wykresy
plt.figure(1)
plt.plot( stopnie , pomiary_t_srednie, 'bo')
plt.plot( stopnie , czas_model , 'b:')
plt.xlabel('Stopien wielomianow')
plt.ylabel('Czas mnożenia wielomianow [s]')
plt.legend(['Wyniki eksperymentu', f'Dopasowanie modelu, a = {np.round(res_1.x[0], 4)}, b {np.round(res_1.x[1], 4)}'])
