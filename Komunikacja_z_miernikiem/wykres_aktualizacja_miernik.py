
from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
import time
matplotlib.use('Qt5Agg')        # Make sure that we are using QT5
from PyQt5 import QtCore, QtWidgets
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import csv
import numpy as np
import pyvisa

#from PyQt5 import QtCore, QtGui, QtWidgets

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class Aparature:
    adres_miernika = 'USB0::0x164E::0x0DAD::TW00042933::INSTR'
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.miernik = rm.open_resource(self.adres_miernika)

    def measurement(self):
        pomiar = self.miernik.query("MEAS:RES?")
        return pomiar



class Figura_wykresu(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        # FigureCanvas.setSizePolicy(self,
        #                            QtWidgets.QSizePolicy.Expanding,
        #                            QtWidgets.QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class Wykres_statyczny(Figura_wykresu):

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

class Wykres_dynamiczny(Figura_wykresu):

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)
        self.nasz_miernik = Aparature()

    def compute_initial_figure(self):
        self.y_var=[random.randint(0, 10) for i in range(10)]
        self.x_var=[i for i in range (10)]
        self.axes.plot(self.x_var,self.y_var, 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        # l = [random.randint(0, 10) for i in range(10)]

        data = float(self.nasz_miernik.measurement())

        print(data)
        with open("test_data_3.csv","a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([time.time(), data])
        self.y_var = np.append(self.y_var, data )
        self.y_var = self.y_var[1 : ]

        self.axes.cla()
        self.axes.plot(self.x_var, self.y_var, 'r')
        self.draw()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(945, 712)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.przycisk2 = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk2.setGeometry(QtCore.QRect(480, 520, 221, 71))
        self.przycisk2.setObjectName("przycisk2")
       
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(100, 80, 22, 351))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
       
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(260, 70, 401, 341))
        self.widget.setObjectName("widget")

        self.l = QtWidgets.QVBoxLayout(self.widget)
        self.dc = Wykres_dynamiczny(self.widget, width=5, height=4, dpi=100)
        self.l.addWidget(self.dc)
       
        MainWindow.setCentralWidget(self.centralwidget)
       
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 26))
        self.menubar.setObjectName("menubar")
       
        MainWindow.setMenuBar(self.menubar)
       
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
       
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.przycisk2.setText(_translate("MainWindow", "napis na przyscisku2"))
        self.przycisk2.clicked.connect(self.dc.update_figure)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
