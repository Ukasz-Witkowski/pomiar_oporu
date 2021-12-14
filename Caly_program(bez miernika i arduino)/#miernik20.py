import pyvisa

class Aparature:
    adres_miernika = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.miernik = rm.open_resource(self.adres_miernika)
        self.otworz

    def ustaw_r(self):
        self.miernik.write("CONF:RES")

    def ustaw_v(self):
        self.miernik.write("CONF:VOLT:DC")

    def otworz(self):
        self.miernik.write("ROUT:OPEN")
    
    def zamknij(self,ch):
        self.miernik.write(f'ROUT:CLOS {ch}')
        print("ch ",ch)
    def mierz(self):
        pomiar = self.miernik.query("READ?") 
        print("pomiar")
        return pomiar


    