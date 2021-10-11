import time
import pyvisa


class Aparature:
    multimeter = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.wielkosc = rm.open_resource(self.multimeter)

    def set(self):
        self.wielkosc.write("ROUT:SCAN:TIMER 7")

    def measurement(self):
        pomiar = self.wielkosc.query("ROUTe:SCAN:TIMER?") 
        return pomiar

aparature = Aparature()

aparature.set()

while True:
    print(aparature.measurement())
    time.sleep(0.5)