import sys
from PyQt5.QtWidgets import QApplication
from MojeOkno import MojeOkno


def main():
    # definiujemy aplikację, tu umieszzzamy nasze okno i widzety
    apka = QApplication(sys.argv)
    # pudełko które przechwouje wszystkie nasze przyciski, napisy itp.
    okno = MojeOkno()
    okno.show()
    # time.sleep(0.5)
    # okno.aktualizuj_wykres([1,2,3,4],[1,4,9,16])

    sys.exit(apka.exec_())           # dzięki temu się nie zamyka od razu


main()  # wywołujemy funkcje main()
