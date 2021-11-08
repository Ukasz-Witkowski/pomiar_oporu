from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MojeOkno(QMainWindow):
    def __init__(self):
        super(MojeOkno,self).__init__()
        self.setGeometry(500,300,800,500)  # dwie poerwsze to współrzędne lewego górnego rogu okinka licząc od lewego górnego rogu ekranu, dwie kolejne to wymiary okienka
        self.setWindowTitle("Program do pomiaru oporu elektryznego")  #nazwa okienka
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self) #tworzymy jakiś napis
        self.label.setText("Zaraz zaczynam pomiar") #wypełniamy go treścią
        self.label.move(400, 100) #Położenie napisu w okienku  

        self.b1=QtWidgets.QPushButton(self)
        self.b1.setText("Click me!")
        self.b1.clicked.connect(self.nacis)

    def nacis(self):
        print("jazda!")
        self.label.setText("klinkąłeś przysicków 100 XD")
        self.update()
    
    def update(self):
        self.label.adjustSize()

def main():
    app = QApplication(sys.argv)    #definiujemy aplikację, tu umieszzzamy nasze okno i widzety 
    win = MojeOkno()             # pudełko które przechwouje wszystkie nasze przyciski, napisy itp.
    win.show() 
    sys.exit(app.exec_()) #dzięki temu się nie zamyka od razu

main()  # make sure to call the function