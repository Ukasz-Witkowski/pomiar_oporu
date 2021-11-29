from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Fig_Can
import sys
import numpy as np
import time

class wykres(Fig_Can):      #dziedziczy po klasie bedącej w jakiejś bibliotece matplotlib
    def __init__(self, parent):

        self.fig, self.ax = plt.subplots()

        super().__init__(self.fig)
        self.setParent(parent)

        self.X = np.arange(0.0, 2.0, 0.01)
        self.Y = 1 + np.sin(2 * np.pi * self.X)
        
        self.line, = self.ax.plot(self.X,self.Y)
        self.ax.set(xlabel='Czas[s]', ylabel='Napięcie[mV]',title='Opis tego co mierzymy')          

class MojeOkno(QMainWindow):
    def __init__(self):  # konstruktor (wykonuje się przy stworzeniu obiektu klasy Moje okno)
        super(MojeOkno,self).__init__()  #wywołuje konstruktor klasy nadrzędnej
        self.setGeometry(100,50,1600,900)  # dwie poerwsze to współrzędne lewego górnego rogu okinka licząc od lewego górnego rogu ekranu, dwie kolejne to wymiary okienka
        self.setWindowTitle("Program do pomiaru oporu elektryznego")  #nazwa okienka
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self) #tworzymy jakiś napis
        self.label.setText("Zaraz zaczynam pomiar") #wypełniamy go treścią
        self.label.adjustSize()
        self.label.move(1000, 100) #Położenie napisu w okienku  

        self.b1=QtWidgets.QPushButton(self)
        self.b1.setText("Click me!")
        self.b1.clicked.connect(self.nacis)
        
        self.b1.move(1000,300)
        self.chart1 = wykres(self)
        #self.aktualizuj_wykres()#[1,2,3,4],[1,4,9,16])
        #self.b1.clicked.connect(self.aktualizuj_wykres)

    def aktualizuj_wykres(self):
        self.chart1.ax.set(xlabel='heheh, zmieniłem oś')
        self.X=[1,2,3,4]
        self.Y=[1,4,9,16]
        #self.chart1.fig.canvas.draw()
        #self.chart1.fig.canvas.flush_events()
        self.chart1.line.set_xdata(self.X)
        self.chart1.line.set_ydata(self.Y)
        self.chart1.ax.relim()
        self.chart1.ax.autoscale_view()
        self.chart1.ax.grid()
        print("hejjj")
        self.update()
        

    def nacis(self):
        print("jazda!")
        self.label.setText("klinkąłeś przysicków 100 XD")
        self.update()
    
    def update(self):
        self.label.adjustSize()

def main():
    apka = QApplication(sys.argv)    # definiujemy aplikację, tu umieszzzamy nasze okno i widzety 
    okno = MojeOkno()                # pudełko które przechwouje wszystkie nasze przyciski, napisy itp.
    okno.show() 
    #time.sleep(0.5)
    #okno.aktualizuj_wykres([1,2,3,4],[1,4,9,16])
    
    sys.exit(apka.exec_())           # dzięki temu się nie zamyka od razu

main()  # wywołujemy funkcje main()