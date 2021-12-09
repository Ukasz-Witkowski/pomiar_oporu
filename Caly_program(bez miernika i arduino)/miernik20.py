import random

class Aparature:
    # adres_miernika = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        print("Polaczono z miernikiem")
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
        print(f'Zamknieto kanal {ch}')
        # self.miernik.write(f'ROUT:CLOS {ch}')
    

    def mierz(self):
        pomiar = random.randint(0, 10)
        return pomiar

