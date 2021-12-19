import random
import time
import numpy as np

class Aparature:
    error=0
    def __init__(self):
        print("Polaczono z miernikiem")
        self.k=0

    def ustaw_r(self):
        print("Usawiono pomiar R")

    def ustaw_v(self):
        print("Ustaiono pomiar V")
        
    def ustaw_r_zakres(self,r):
        print("Ustawiono zakres r: ",r)
    
    def ustaw_r4_zakres(self,r):
        print("Ustawiono zakres r4: ",r)

    def otworz(self):
        print("Otawrto kanaøy")
    
    def zamknij(self,ch):
        self.k=ch
        print(f'Zamknieto kanal {ch}')
    

    def mierz(self):
        print("mierz")
        if(self.k%5==0):
            pomiar=random.randint(0,10)/100
        if(self.k%5==1):
            pomiar=np.exp(np.sin(time.time()/30))+random.randint(0,10)/200
        if(self.k%5==2):
            pomiar=np.sin(time.time()/30)**5+random.randint(0,10)/200
        if(self.k%5==3):
            pomiar=np.log(np.sin(time.time()/30)+1.2)+random.randint(0,10)/200
        if(self.k%5==4):
            pomiar = np.sin(time.time()/100)+random.randint(0,10)/200
        return pomiar

