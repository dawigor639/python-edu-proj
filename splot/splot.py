# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import stats

def overlapSave(x, y, N):
    Y = np.conj(np.fft.fft(y, N)) 
    M = len(y) #dlugosc ciagu y 
    L = N - M + 1 #nowa dlugosc
    wynik = np.empty_like(x)
    blok = np.zeros(N, dtype=x.dtype)
    przesuniecie = 0
    while ( przesuniecie < len(x) ):
        blok_poz = (N, len(x)-przesuniecie)[(przesuniecie + N > len(x)) == True]
        blok[ blok_poz:] = 0
        blok[:blok_poz] = x[przesuniecie:przesuniecie + blok_poz]
        blok = np.fft.ifft(np.fft.fft(blok) * Y)
        
        wynik_poz = (L, len(x)-przesuniecie)[(przesuniecie + L > len(x)) == True]
        wynik[przesuniecie:przesuniecie + wynik_poz] = blok[:wynik_poz]
        przesuniecie += L
        
    if np.iscomplexobj(wynik):
        return wynik
    else:
        return np.real(wynik)   

def nastPot2(n):
    l = 0
    if (n and not(n & (n - 1))):
        return n
    while( n != 0):
        n >>= 1
        l += 1
    return 1 << l

# Test poprawnosci #
x = np.random.randn(1024)
y = np.random.randn(5)
nconv = x.size + y.size - 1
oczekiwania = np.fft.ifft(np.fft.fft(x, nconv) * np.conj(np.fft.fft(y, nconv)))[:x.size]
testStart = time.time()
testowana_funkcja = overlapSave(x, y, 1024)
testKoniec  = time.time() - testStart
Wynik_testu = np.allclose(testowana_funkcja, oczekiwania)
# Test poprawnosci #

#Splatanie ciagow
y=[1,1,1,1,-1] #dany ciag y
M=len(y)
ile=60 #liczba ciagow x
ile_N=4 #liczba testowanych N dla kazdej dlugosci ciagu x
dlugosci=np.linspace(1024,1024*1024,ile) #dlugosci ciagow x
dlugosci= np.round ( np.array(dlugosci) ).astype(int)


#dobor N jako poteg 2 
N2 = [] #dlugosc bloku 
potegi_2=[]
start_poteg=128 # spelnia warunek N>2*M
for i in range(0,ile_N):
    potegi_2.append(start_poteg)
    start_poteg=start_poteg*2
potegi_2 = [int(i) for i in potegi_2] #float -> int
for i in range(0,ile):
    N2.append( potegi_2 ) 

#tworzenie list z losowymi liczbami o dlugosciach z zakresu od 1024 do 1024^2
x = [] #losowe liczby
for i in range(0,ile):
    x.append( np.random.rand(dlugosci[i]) )

#zmiana sposobu przechowywania danych
N2=np.array(N2)
dlugosci=dlugosci.reshape(len(dlugosci),1)
#pomiary czasow dla danych dlugosci x i N    
pomiary_t=np.zeros((ile,ile_N))#tablica czasow dla danej dlugosci i n
Ti=0 #czas dla i-tej listy    
for i in range(0,ile): #iteracja po dlugosciach
    for j in range(0,ile_N): #iteracja po N
        start_Ti = time.time() #pomiar czasu start
        overlapSave(x[i],y,N2[i,j]) 
        koniec_Ti = time.time() #pomiar czasu stop
        Ti = koniec_Ti - start_Ti
        pomiary_t[i,j]=Ti
    print('wykonano overlapSave dla danego x,y i roznych N','w czasie:',np.sum(pomiary_t[i,:]),'s ',int(i/ile*100),'%')

#### Model - złożonosc obliczeniowa overlap save ###

#dopasowanie modelu
stale_a=[]
modele_t=[]
for i in range (0,4): 
    a, *param = stats.mstats.linregress(  dlugosci/potegi_2[i] , pomiary_t[:,i]  ) #
    stale_a.append(a)
    modele_t.append( (stale_a[i]) * (dlugosci/potegi_2[i])   )

#wykresy
fig=plt.figure(1)
plt.plot( dlugosci , pomiary_t[:,0] , 'b.', label=f"Wyniki pomiarow, N={potegi_2[0]}" )
plt.plot( dlugosci , pomiary_t[:,1] , 'c.', label=f"Wyniki pomiarow, N={potegi_2[1]}" )
plt.plot( dlugosci , pomiary_t[:,2] , 'g.', label=f"Wyniki pomiarow, N={potegi_2[2]}" )
plt.plot( dlugosci , pomiary_t[:,3] , 'm.', label=f"Wyniki pomiarow, N={potegi_2[3]}" )

plt.plot( dlugosci , modele_t[0] , 'b:', label=f"Dopasowanie do modelu, N={potegi_2[0]}" )
plt.plot( dlugosci , modele_t[1] , 'c:', label=f"Dopasowanie do modelu, N={potegi_2[1]}" )
plt.plot( dlugosci , modele_t[2] , 'g:', label=f"Dopasowanie do modelu, N={potegi_2[2]}" )
plt.plot( dlugosci , modele_t[3] , 'm:', label=f"Dopasowanie do modelu, N={potegi_2[3]}" )

plt.title("Wzor: $a*obl*(N_x/N)$ \n gdzie $N_x$ - dł. x, N - dł. bloku,  obl - zlozonosc splotu $O(N\log_2(N))$, a - stala (predkosc pc)")
plt.xlabel('Dlugosc ciagu x')
plt.ylabel('Czas wykonania overlap-save [s]')
plt.legend()
fig.set_figheight(7)
fig.set_figwidth(7)
