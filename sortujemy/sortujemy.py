# -*- coding: utf-8 -*-

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import copy

### Klasa ###

class Kopiec(list):
    def __init__(self, lista=None):
        self.kopiec_lista = []
        #tworze kopiec dostepny pod polem 'kopiec_lista' z podanej listy 
        if lista is not None:
            for x in lista:
                self.dodaj(x)

    def przesun_dol(self,kopiec, i):
        rodzic_i = (i - 1) // 2
        #jesli trafilismy na węzeł główny
        if rodzic_i < 0:
            return
            
       
        if kopiec[i] > kopiec[rodzic_i]:
            kopiec[i], kopiec[rodzic_i] = kopiec[rodzic_i] , kopiec[i]
            self.przesun_dol(kopiec, rodzic_i)

    def przesun_gora(self,kopiec, i):
        dziecko_i = 2 * i + 1
        #jesli trafilismy na koniec kopca
        if dziecko_i >= len(kopiec):
            return

        if dziecko_i + 1 < len(kopiec) and kopiec[dziecko_i] < kopiec[dziecko_i + 1]:
            dziecko_i += 1

        if kopiec[dziecko_i] > kopiec[i]:
            kopiec[dziecko_i], kopiec[i] = kopiec[i] , kopiec[dziecko_i]
            self.przesun_gora(kopiec, dziecko_i)

    def dodaj(self, value):
        self.kopiec_lista.append(value)
        self.przesun_dol(self.kopiec_lista, len(self) - 1)

    def usun(kopiec):
        kopiec.kopiec_lista[len(kopiec) - 1], kopiec.kopiec_lista[0] =  kopiec.kopiec_lista[0] ,  kopiec.kopiec_lista[len(kopiec) - 1]
        x = kopiec.kopiec_lista.pop()
        kopiec.przesun_gora(kopiec.kopiec_lista, 0)
        return x

    def __len__(self):
        return len(self.kopiec_lista)

    def kopiec_sort(self):
        kopiec = copy.deepcopy(self)
        posortowane = []
        while len(kopiec) > 0:
            posortowane.append(kopiec.usun())
        return posortowane     
    #testowanie poprawnosci sortowania 
    def test_sort(self,x):
        if (x==sorted(x,reverse=True)):
            return True
        else:
            return False 
       
       
       
#parametry       
maks=10**6 #maks wartosci liczb (+/-)    
M=0 #liczba sortowanych liczb / dlugosc listy
N=12 #liczba list

### badanie czasu sortowania dla 100 tys liczb ###
liczby_100=np.random.randint(-maks,maks, size=(100000)).tolist()
T0=0 #czas sortowania dla (M=100000)
kopiec_t0=Kopiec(liczby_100) #tworze obiekt klasy Kopiec i laduje liste 100tys elementow
start_T0 = time.time()  
kopiec_t0.kopiec_sort() #sortowanie   
koniec_T0 = time.time()
T0 = koniec_T0 - start_T0

### badanie czasu sortowania dla 12 list liczb o dlugosci od 1*10^6 do 5*10^6 ###
dlugosci=  np.linspace(10**6,5*10**6,12) #dlugosci 12 list
dlugosci = [int(np.round(i)) for i in dlugosci]

#tworzenie 12-stu list z losowymi liczbami o dlugosciach od 1*10^6 do 5*10^6 
liczby = []
for i in range(0,N):
    liczby.append( np.random.randint(-maks,maks, size=( dlugosci[i] )).tolist() )

#sortowanie 12 list 
pomiary_t=[]
Ti=0 #czas sortowania dla i-tej listy
for i in range(0,N):
    x=Kopiec(liczby[i])
    start_Ti = time.time() #pomiar czasu start
    x.kopiec_sort()
    koniec_Ti = time.time() #pomiar czasu stop
    Ti = koniec_Ti - start_Ti
    pomiary_t.append(Ti)
    print('posortowano liste nr:',i+1, 'w czasie:',Ti,' s')
    #print(x.test_sort(x.kopiec_sort())) #sprawdzanie poprawnosci sortowania

pomiary_t_do_t0=np.array(pomiary_t)/T0 # wartosci T do T0
#regresja liniowa
a, *param = stats.linregress( np.log2(np.array(pomiary_t)/(T0 * np.log2(np.array(dlugosci)))), np.log2(np.array(dlugosci)) )  
#obliczenie czasu wynikajacego z dopasowania modelu 1
T = (np.array(dlugosci) ** a * np.log2(np.array(dlugosci)))/((10**5) ** a * np.log(10**5))
    
plt.plot(dlugosci, pomiary_t_do_t0,'bo',)
plt.plot(dlugosci, T,'b:')
plt.title("T/T0 do dlugosci sortowanej listy")
plt.xlabel("Liczba elementów")
plt.ylabel("T/T0")
plt.legend(["Wyniki eksperymentalne", f"Dopasowanie modelu, a = {np.round(a, 4)}"])
plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))