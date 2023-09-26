# -*- coding: utf-8 -*-

import time

start = time.time() #start odliczania czasu

def sqrt(x):
    return x**(0.5)

def zaokr(x):
    return round(x, 2)

def blad(x):
    if (abs(x-7.11)<=0.00000001):
        return True

#lista wynikow wiersze [a , b, c, d]
list_abcd = []

ilosc_porownan=0

for a in range (1,712):
    
    a=a/100
    
    for b in range (1,712):
        
        b=b/100
        
        c = -(100*a**2*b + 100*a*b**2 - 711*a*b + sqrt(a*b*(a*b*(100*a + 100*b - 711)**2 - 284400)))/(200*a*b) 
        d = (-100*a**2*b - 100*a*b**2 + 711*a*b + sqrt(a*b*(a*b*(100*a + 100*b - 711)**2 - 284400)))/(200*a*b)
        cc = (-100*a**2*b - 100*a*b**2 + 711*a*b + sqrt(a*b*(a*b*(100*a + 100*b - 711)**2 - 284400)))/(200*a*b)
        dd = -(100*a**2*b + 100*a*b**2 - 711*a*b + sqrt(a*b*(a*b*(100*a + 100*b - 711)**2 - 284400)))/(200*a*b)
        
        ilosc_porownan+=1 #sprawdzenie czy zespolone 
        if( not isinstance(c*d, complex) ):
            
            if ( blad(a*b*zaokr(c)*zaokr(d)) and blad(a+b+zaokr(c)+zaokr(d)) and c>0 and d>0 ):
                list_abcd.append([a,b,zaokr(c),zaokr(d)])
            
        ilosc_porownan+=1 #sprawdzenie czy zespolone       
        if( not isinstance(cc*dd, complex) ):
             
            if ( blad(a*b*zaokr(cc)*zaokr(dd)) and blad(a+b+zaokr(cc)+zaokr(dd)) and cc>0 and dd>0 ):
                list_abcd.append([a,b,zaokr(cc),zaokr(dd)])
               

end = time.time()  #koniec odliczania czasu
czas= end - start

print('czas [s] =', czas, ', ilosc_porownan  =', ilosc_porownan) #czas wykonania obliczen i ilosc sprawdzonych warunkow