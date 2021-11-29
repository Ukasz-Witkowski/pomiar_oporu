#program wykonuje pętlę po wszystkich kanałach zamykając po kolei każdy i wypisyjąc listę, które są zapisane a któe otwarte

import time
import pyvisa

class Aparature:
    multimeter = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.wielkosc = rm.open_resource(self.multimeter)

    def ope(self):
        self.wielkosc.write("ROUT:OPEN")

    def clo(self,ch):
        self.wielkosc.write(f'ROUT:CLOS {ch}')

    def measurement(self):
        pomiar = self.wielkosc.query("ROUTe:CLOSe?") 
        return pomiar

aparature = Aparature()

aparature.ope()
for i in range(20):
    aparature.clo(i+1)
    time.sleep(0.5)
    print(aparature.measurement())


