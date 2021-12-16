import random
import time
import numpy as np

class Aparature:
    # adres_miernika = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        print("Polaczono z miernikiem")
        self.k=0
        # rm = pyvisa.ResourceManager()
        # self.miernik = rm.open_resource(self.adres_miernika)

    def ustaw_r(self):
        print("Usawiono pomiar R")
        #self.miernik.write("CONF:RES")

    def ustaw_v(self):
        print("Ustaiono pomiar V")
        # self.miernik.write("CONF:VOLT:DC")

    def otworz(self):
        print("Otawrto kanaøy")
        # self.miernik.write("ROUT:OPEN")
    
    def zamknij(self,ch):
        self.k=ch
        print(f'Zamknieto kanal {ch}')
        # self.miernik.write(f'ROUT:CLOS {ch}')
    

    def mierz(self):
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

