import sys
from PyQt5.QtWidgets import QApplication
from MojeOkno import MojeOkno

def main():
    apka = QApplication(sys.argv)
    okno = MojeOkno()
    okno.show()
    sys.exit(apka.exec_())           # dzięki temu się nie zamyka od razu

main()  # wywołujemy funkcje main()
