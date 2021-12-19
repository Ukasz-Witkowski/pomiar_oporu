from numpy import NaN
import pyvisa

class Aparature:
    adres_miernika = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    error=0
    def __init__(self):
        try:
            rm = pyvisa.ResourceManager()
            self.miernik = rm.open_resource(self.adres_miernika)
            self.ustaw_r
            self.otworz
        except:
            print("nie ma miernika")
            self.error=1

    def ustaw_r(self):
        self.miernik.write("CONF:RES")
    
    def ustaw_r4(self):
        self.miernik.write("CONF:FRES")


    def ustaw_r_zakres(self,r):
        self.miernik.write(f"CONF:RES {r}")
        
    def ustaw_r4_zakres(self,r):
        self.miernik.write(f"CONF:FRES {r}")
        

    def ustaw_v(self):
        self.miernik.write("CONF:VOLT:DC")

    def otworz(self):
        self.miernik.write("ROUT:OPEN")
    
    def zamknij(self,ch):
        self.miernik.write(f'ROUT:CLOS {ch}')
    
    def mierz(self):
        pomiar = self.miernik.query("READ?")
        print(pomiar)
        if(float(pomiar)>10**10):
            pomiar=NaN 
        return pomiar


    