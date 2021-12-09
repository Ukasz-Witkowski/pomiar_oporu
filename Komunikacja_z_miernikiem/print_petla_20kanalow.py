#program który wykonuje pomiar co 2 s na kolejnych kanałach i wypisuje wartośc w terminalu

import time
import pyvisa


class Aparature:
    multimeter = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.wielkosc = rm.open_resource(self.multimeter)

    def set_r(self):
        self.wielkosc.write("CONF:RES")

    def set_v(self,a):
        # self.wielkosc.write(f'ROUT:SCAN:FUNC {a},"VOLT:DC"')
        self.wielkosc.write("CONF:VOLT:DC")

    def ope(self):
        self.wielkosc.write("ROUT:OPEN")
    
    def clo(self,ch):
        self.wielkosc.write(f'ROUT:CLOS {ch}')

    def f_query(self,a):
        pomiar = self.wielkosc.query(f'ROUT:SCAN:FUNC? {a}') 
        return pomiar

    def clo_query(self):
        pomiar = self.wielkosc.query("ROUTe:CLOSe?") 
        return pomiar
    
    def measure(self):
        pomiar = self.wielkosc.query("READ?") 
        return pomiar

aparature = Aparature()

aparature.clo(19)

# time.sleep(0.5)

# aparature.set_r()

time.sleep(1)

aparature.set_v(1)

time.sleep(0.5)

while True:
    for i in range(20):
        aparature.clo(i+1)
        time.sleep(0.5)
        print(str(i+1)+". "+str(aparature.measure())) 
        time.sleep(0.5)
    print("--------------")
    time.sleep(3)

    