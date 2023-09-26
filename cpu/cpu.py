# -*- coding: utf-8 -*-
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import time

def obliczBlok(blok,Y): 
   return np.fft.ifft(np.fft.fft(blok) * Y)

# Zmodyfikowany overlapSave  #
def overlapSave(x, y, N):
    x=x.astype(complex)
    y=y.astype(complex)
    Y = np.conj(np.fft.fft(y, N)) 
    M = len(y) #dlugosc ciagu y 
    L = N - M + 1 #nowa dlugosc
    blok = np.zeros(N, dtype=x.dtype)
    przesuniecie = 0
    i=0
    while ( przesuniecie < len(x) ): #Zlecanie wszystkich zadan 
        blok_poz = (N, len(x)-przesuniecie)[(przesuniecie + N > len(x)) == True]
        blok[ blok_poz:] = 0
        blok[:blok_poz] = x[przesuniecie:przesuniecie + blok_poz]
        wynik_poz = (L, len(x)-przesuniecie)[(przesuniecie + L > len(x)) == True]
        in_queue.put((blok,Y,przesuniecie,wynik_poz,i)) #Wpisanie danych do kolejki
        przesuniecie += L
        i += 1
    in_queue.join()
        
    #pozyskane wyniki
    return wyniki

# Zmodyfikowana klasa  #
class starter(multiprocessing.Process):
    
    def __init__(self, datain_queue,numer, wyniki):
        super().__init__()
        self.datain_queue = datain_queue
        self.numer = numer
        self.wyniki = wyniki

    def run(self):
        while True:
            try:
                dane = self.datain_queue.get()
                self.niewolnik(dane)
            finally:
                self.datain_queue.task_done()
        return
    
    def niewolnik(self,dane): # pracuje jak mu każą
        przesuniecie = dane[2]
        wynik_poz = dane[3] 
        for i in range(0,3000): #niewolnik oblicza ten sam splot 3000 razy (SYMULACJA)
            wynik =  obliczBlok(dane[0], dane[1]) #oblicza blok na podstawie danych
        self.wyniki[przesuniecie:przesuniecie + wynik_poz]=wynik[:wynik_poz]  #do wynikow wpisuje identyfikator i obliczony blok
        return()

if __name__ == '__main__':
    
    '''
    # Test poprawnosci #
    
    #jeden deamon
    jobs = [] #rejestr deamonow
    in_queue = multiprocessing.JoinableQueue() # kolejka z danymi
    wyniki=multiprocessing.Manager().list()    # kolejka z wynikami
    zadanie = starter(in_queue, 1, wyniki)
    zadanie.daemon = True
    zadanie.start()
    jobs.append(zadanie)
    x = np.random.choice([-1, 1],size=(1024))
    y = np.random.choice([-1, 1],size=(5))
    nconv = x.size + y.size - 1
    oczekiwania = np.fft.ifft(np.fft.fft(x, nconv) * np.conj(np.fft.fft(y, nconv)))[:x.size]
    testStart = time.time()
    testowana_funkcja = overlapSave(x, y, 1024)
    testKoniec  = time.time() - testStart
    Wynik_testu = np.allclose(testowana_funkcja, oczekiwania)
    print(testKoniec)
    # Test poprawnosci #
    '''
    
## Przygotowanie danych ##

    pomiary_d=[]
    pomiary_k=[]

    ilosc_splotow = 2 #kazdy deamon oblicza splot 3000 razy
    K = 2**20 #dlugosc ciagu (dlugiego)
    M = 2**10 #dlugosc ciagu (krotkiego)
    N = 4096  #dlugosc segmentu N
    
    xd = np.random.choice([-1, 1],size=(K)) #jeden losowy ciag dlugi
    xk = np.random.choice([-1, 1],size=(M)) #jeden losowy ciag krotki

    max_d=7 # maksymalna_liczba_deamonow-1, cpu 4 rdzenie
    y=np.array([1,1,1,1,-1],dtype=int)
    
    jobs = [] #rejestr deamonow
    in_queue = multiprocessing.JoinableQueue() # kolejka z danymi
    wyniki=multiprocessing.Manager().list()    # kolejka z wynikami
    
    for i in range(1,max_d): #petla po ilosci deamonow (od 1 do 5 deamonow)
        #Utworzenie daemona (i)
        zadanie = starter(in_queue, i, wyniki)
        zadanie.daemon = True
        zadanie.start()
        jobs.append(zadanie)
        
        start = time.time() #pomiar czasu start (krotki)
        overlapSave(xk, y, N)
        ti = time.time() - start #pomiar czasu stop (krotki)
        pomiary_k.append(ti)
        
        start= time.time() #pomiar czasu start (dlugi)
        overlapSave(xd, y, N)
        ti = time.time() - start #pomiar czasu stop (dlugi)
        pomiary_d.append(ti)
        
    #Wykres zależności czasu obliczeń od liczby uruchomionych daemonów.
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Symulacja (liczba rdzeni = 4)')
    ax1.plot(np.linspace(1,max_d-1,max_d-1) , pomiary_d , 'b-o', label="Ciag dlugi, $K=2^{20}$")
    ax2.plot(np.linspace(1,max_d-1,max_d-1) , pomiary_k , 'c-o', label="Ciag krotki, $M=2^{10}$")
    ax1.set_xlabel('Liczba uruchomionych daemonów')
    ax2.set_xlabel('Liczba uruchomionych daemonów')
    ax1.set_ylabel('Czas obliczen (R=3000) [s]')
    ax2.set_ylabel('Czas obliczen (R=3000) [s]')
    ax1.legend()
    ax2.legend()
    fig.subplots_adjust(hspace=0.3)
    fig.set_figheight(6)