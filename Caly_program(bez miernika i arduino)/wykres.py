from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
from numpy import NaN, arange, sin, pi
import numpy as np
import miernik20
import csv
import time
import json

class Figura_wykresu(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass

class Wykres_dynamiczny_1(Figura_wykresu):
    def load_default_path(self):
        f = open('config.json')
        data = json.load(f)
        default_path = data['default_path']
        f.close()
        return default_path

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1000)
        self.nasz_miernik = miernik20.Aparature()
        self.default_path = self.load_default_path()

    def compute_initial_figure(self):
        self.y_var=[random.randint(0, 10) for i in range(10)]
        self.x_var=[i for i in range (10)]
        self.axes.plot(self.x_var,self.y_var, 'r')

    def update_figure(self):

        data = float(self.nasz_miernik.mierz())
        #print(data)
        # print(self.default_path)
        with open(self.default_path,"a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([time.time(), data])
        self.y_var = np.append(self.y_var, data )
        self.y_var = self.y_var[1 : ]

        self.axes.cla()
        self.axes.plot(self.x_var, self.y_var, 'b')
        self.draw()

class Wykres_temp(Figura_wykresu):

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.dane=[[NaN,NaN]]
        self.axes.plot([],[], 'r')

    def update_figure(self):
        self.axes.cla()
        self.axes.plot(self.dane[:,0], self.dane[:,1], 'r')
        self.draw()

class Wykres_probka(Figura_wykresu):
    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.dane=[[NaN,NaN]]
        self.axes.plot([],[], 'b')

    def update_figure(self):
        self.axes.cla()
        self.axes.plot(self.dane[:,0], self.dane[:,1], 'b')
        self.draw()


class Wykres_rysowanie(Figura_wykresu):

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.x_var=[i for i in range (10)]
        self.y_var=[0 for i in range(10)]
        self.axes.plot(self.x_var,self.y_var, 'b')

    def update_figure(self,x,y):
        self.x_var=x
        self.y_var=y
        self.axes.cla()
        self.axes.plot(self.x_var, self.y_var, 'b')
        self.draw()
        