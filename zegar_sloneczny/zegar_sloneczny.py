# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def zegar1(szer_geogr,godz_pracy,nn,nazwa):
    t_dod=np.arange( 0 , godz_pracy[1]-12+1 , 1 ) #tylko polowa zakresu (symetria)
    t = np.deg2rad((t_dod) * 15) #czas w rad

    godziny=np.arange(12,godz_pracy[1]+1,1).astype(int) #od 12 do konca
    godziny= list(godziny) + list(reversed(list(godziny-7)[1:])) #od 12 do zachodu + wstecz od 12 do wschodu bez 12

    #wstawienie szerokosci geograficznej i t do rownania 
    h_polowa=np.arctan(np.sin(szer_geogr_kair)*np.tan(t)) #wskazania godzin h
    h=np.array( list(h_polowa))
    h=np.where(h < 0, h+(np.pi), h) #poprawa dla katow ujemnych (rysunek)
    h=np.concatenate([h,-h[1:]]) #polaczenie godzin >=12 i <12

    #### odeint #### 
    def drdt(r,t):
        return  (1-(r**2*(1/ (( np.cos(t)**2 + np.sin(szer_geogr)**2*np.sin(t)**2 )**2)) )) # = r'(t)^2
    r0 = nn
    rt = odeint(drdt, y0=r0, t=t) 
    rt = np.array( rt )
    rt = np.sqrt(rt) # = r'(t)
    #### odeint ####

    #Wykres punktow dla godzin w Kairze
    kat = h
    promien = 1
    x = promien * np.cos( kat ) 
    y = promien * np.sin( kat ) 
    fig, ax = plt.subplots( 1 ) 
    ax.plot( x, y , 'bo' , label='Godziny') 
    ax.set_aspect( 1 ) 
    #indeksy
    for i in range(len(x)):
        ax.text(x[i], y[i], " "+str((godziny)[i]))
    ax.grid(True) 
    ax.set_xlim(-1,1.2)
    ax.set_title( f"Zegar sloneczny {nazwa}" ) 
    
    #rysowanie lini dla kazdej godziny
    for i in range(0,len(x)):
        ax.plot([0,x[i]], [0, y[i]], 'b-')

    #Wykres rekompensaty dla godzin w Kairze
    promien=list(rt) + list(rt)[1:]
    kat=h.reshape(len(h),1)
    xr = promien * np.cos( kat ) 
    yr = promien * np.sin( kat ) 
    ax.plot( xr, yr , 'ro' , label='Poprawka dla niejednostajnego ruchu cienia') 
    ax.legend()
    ax.legend(bbox_to_anchor =(1.1, -0.1))

def zegar2(szer_geogr,godz_pracy,nn,nazwa):
    t_dod=np.arange( 0 , godz_pracy[1]-12+1 , 1 ) #tylko polowa zakresu (symetria)
    t = np.deg2rad((t_dod) * 15) #czas w rad

    godziny=np.arange(12,godz_pracy[1]+1,1).astype(int) #od 12 do konca
    godziny= list(godziny) + list(reversed(list(godziny-9)[2:])) #od 12 do zachodu + wstecz od 12 do wschodu bez 12

    #wstawienie szerokosci geograficznej i t do rownania 
    h_polowa=np.arctan(np.sin(szer_geogr_kair)*np.tan(t)) #wskazania godzin h
    h=np.array( list(h_polowa))
    h=np.where(h < 0, h+(np.pi), h) #poprawa dla katow ujemnych (rysunek)
    h=np.concatenate([h,-h[1:-1]]) #polaczenie godzin >=12 i <12
    
    #### odeint #### 
    def drdt(r,t):
        return  (1-(r**2*(1/ (( np.cos(t)**2 + np.sin(szer_geogr)**2*np.sin(t)**2 )**2)) )) # = r'(t)^2
    r0 = nn
    rt = odeint(drdt, y0=r0, t=t) 
    rt = np.array( rt )
    rt = np.sqrt(rt) # = r'(t)
    #### odeint ####
    
    #Wykres punktow dla godzin w Kairze
    kat = h
    promien = 1
    x = promien * np.cos( kat ) 
    y = promien * np.sin( kat ) 
    fig, ax = plt.subplots( 1 ) 
    ax.plot( x, y , 'bo' , label='Godziny') 
    ax.set_aspect( 1 ) 
    #indeksy
    for i in range(len(x)):
        ax.text(x[i], y[i], " "+str((godziny)[i]))
    ax.grid(True) 
    ax.set_xlim(-1,1.2)
    ax.set_title( f"Zegar sloneczny {nazwa}" ) 
    
    #rysowanie lini dla kazdej godziny
    for i in range(0,len(x)):
        ax.plot([0,x[i]], [0, y[i]], 'b-')

    #Wykres rekompensaty dla godzin w Kairze
    promien=list(rt) + list(rt)[1:-1]
    kat=h.reshape(len(h),1)
    xr = promien * np.cos( kat ) 
    yr = promien * np.sin( kat ) 
    ax.plot( xr, yr , 'ro' , label='Poprawka dla niejednostajnego ruchu cienia') 
    ax.legend()
    ax.legend(bbox_to_anchor =(1.1, -0.1))

#zegar kair
szer_geogr_kair=np.deg2rad(29.979167)    
godz_pracy_kair=[6,18]    
zegar1(szer_geogr_kair,godz_pracy_kair,1,"Kair 29.979$^\circ$N")

#zegar gliwice
szer_geogr_gliwice=np.deg2rad(50.288204)  
godz_pracy_gliwice=[5,20] 
zegar2(szer_geogr_gliwice,godz_pracy_gliwice,1,"Gliwice 50.288$^\circ$N")
