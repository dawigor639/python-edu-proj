# -*- coding: utf-8 -*-

import numpy as np

def zysk(x):
    wyn = np.where(np.logical_or(x == 1 , x == 6), 1, x)
    wyn = np.where(np.logical_or(x == 2 , x == 7), 2, wyn)
    wyn = np.where(np.logical_or(x == 4 , x == 9), -1, wyn)
    wyn = np.where(np.logical_or(x == 3 , x == 8), -2, wyn)
    wyn = np.where(x==5, 0, wyn)
    return wyn

#punkt 1 

n=1500 #ilosc klientow
m=50   #ilosc sklepow
tablica1=np.zeros((10,4)) #tablica punkt 1 w zad2 
cena_promocyjna = 9*np.ones((n,m))

for i in range(11):
    
    kup_produkty=np.random.poisson(i, (n,m))
    koniec_ceny_promocyjnej = (cena_promocyjna * kup_produkty) % 10
    zysk_klienta=zysk(koniec_ceny_promocyjnej)
    zysk_sklepu=(-1)*zysk_klienta
    zysk_klienta=np.sum(zysk_klienta,1)
    zysk_sklepu=np.sum(zysk_sklepu,0)

    tablica1[i-1,0]=np.max(zysk_klienta)
    tablica1[i-1,1]=np.min(zysk_klienta)
    tablica1[i-1,2]=np.max(zysk_sklepu)
    tablica1[i-1,3]=np.min(zysk_sklepu)
    
#punkt 2  

def sum_ceny_2(x):
    los_koniec = np.random.randint(10, size = x)
    koniec = np.sum(los_koniec)%10
    return koniec

koniec_ceny_2 = np.vectorize(sum_ceny_2)

tablica2=np.zeros((10,4)) #tablica punkt 2 w zad2 

for i in range(11):
    
    kup_produkty=np.random.poisson(i, (n,m))
    koniec_ceny = koniec_ceny_2(kup_produkty)
    zysk_klienta=zysk(koniec_ceny)
    zysk_sklepu=(-1)*zysk_klienta
    zysk_klienta=np.sum(zysk_klienta,1)
    zysk_sklepu=np.sum(zysk_sklepu,0)

    tablica2[i-1,0]=np.max(zysk_klienta)
    tablica2[i-1,1]=np.min(zysk_klienta)
    tablica2[i-1,2]=np.max(zysk_sklepu)
    tablica2[i-1,3]=np.min(zysk_sklepu)

#punkt 3 

liczby_benford = np.linspace(1,10,10)
a = 1/(np.sum(np.log10(1+1/liczby_benford)))
benford_prawd = a * np.log10(1 + 1/liczby_benford)   
    

def sum_ceny_3(x):
    los_koniec = np.random.choice(liczby_benford%10, p=benford_prawd, size=x)
    koniec = np.sum(los_koniec)%10
    return koniec

koniec_ceny_3 = np.vectorize(sum_ceny_3)

tablica3=np.zeros((10,4)) #tablica punkt 3 w zad2 

for i in range(11):
    
    kup_produkty=np.random.poisson(i, (n,m))
    koniec_ceny = koniec_ceny_3(kup_produkty)
    zysk_klienta=zysk(koniec_ceny)
    zysk_sklepu=(-1)*zysk_klienta
    zysk_klienta=np.sum(zysk_klienta,1)
    zysk_sklepu=np.sum(zysk_sklepu,0)

    tablica3[i-1,0]=np.max(zysk_klienta)
    tablica3[i-1,1]=np.min(zysk_klienta)
    tablica3[i-1,2]=np.max(zysk_sklepu)
    tablica3[i-1,3]=np.min(zysk_sklepu)
