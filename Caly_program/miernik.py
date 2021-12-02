import pyvisa

class Aparature:
    adres_miernika = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.miernik = rm.open_resource(self.adres_miernika)

    def mierz(self):
        pomiar = self.miernik.query("MEAS:RES?")
        return pomiar