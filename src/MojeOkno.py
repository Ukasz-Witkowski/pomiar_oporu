from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
from wykres import wykres
import random


class MojeOkno(QMainWindow):
    # def __init__(self):  # konstruktor (wykonuje się przy stworzeniu obiektu klasy Moje okno)
    #     # wywołuje konstruktor klasy nadrzędnej
    #     super(MojeOkno, self).__init__()
    #     # dwie poerwsze to współrzędne lewego górnego rogu okinka licząc od lewego górnego rogu ekranu, dwie kolejne to wymiary okienka
    #     self.setGeometry(100, 50, 1600, 900)
    #     self.setWindowTitle(
    #         "Program do pomiaru oporu elektryznego")  # nazwa okienka
    #     self.initUI()

    # def initUI(self):
    #     self.label = QtWidgets.QLabel(self)  # tworzymy jakiś napis
    #     self.label.setText("Zaraz zaczynam pomiar")  # wypełniamy go treścią
    #     self.label.adjustSize()
    #     self.label.move(1000, 100)  # Położenie napisu w okienku

    #     self.b1 = QtWidgets.QPushButton(self)
    #     self.b1.setText("Click me!")
    #     self.b1.clicked.connect(self.nacis)

    #     self.b1.move(1000, 300)
    #     self.chart1 = wykres(self)
    #     # self.aktualizuj_wykres()#[1,2,3,4],[1,4,9,16])
    #     self.b1.clicked.connect(self.aktualizuj_wykres)

    # def aktualizuj_wykres(self):
    #     self.chart1.ax.remove()
    #     self.chart1.ax.set(xlabel='heheh, zmieniłem oś')
    #     self.X = [1, 2, 3, 4]
    #     self.Y = [1, 4, 9, 16]
    #     # self.chart1.fig.canvas.draw()
    #     # self.chart1.fig.canvas.flush_events()
    #     self.chart1.line.set_xdata(self.X)
    #     self.chart1.line.set_ydata(self.Y)
    #     self.chart1.ax.relim()
    #     self.chart1.ax.autoscale_view()
    #     self.chart1.ax.grid()
    #     print("hejjj")

    # def nacis(self):
    #     print("jazda!")
    #     self.label.setText("klinkąłeś przysicków 100 XD")
    #     self.update()

    # def update(self):
    #     self.label.adjustSize()
    
    def nacis(self):
        print("jazda!")
        self.label.setText("klinkąłeś przysicków 100 XD")
        self.update()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def __init__(self):
        super(MojeOkno, self).__init__()
        self.setGeometry(100, 50, 800, 600)
        self.setWindowTitle(
            "Program do pomiaru oporu elektryznego")  # nazwa okienka
        self.initUI()

        self.canvas = wykres(self, width=21, height=37, dpi=100)
        self.label =  QtWidgets.QVBoxLayout()
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(130, 90, 801, 451))
        self.label.addWidget(self.canvas)

        n_data = 20
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)  # tworzymy jakiś napis
        self.label.setText("Zaraz zaczynam pomiar")  # wypełniamy go treścią
        self.label.adjustSize()
        self.label.move(1000, 100)  # Położenie napisu w okienku

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Click me!")
        self.b1.clicked.connect(self.nacis)

    
        self.chart1 = wykres(self)
        self.chart1.move(1000, 300)
        self.b1.clicked.connect(self.update_plot)

