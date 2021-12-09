from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
from numpy import arange, sin, pi
import numpy as np

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

class Wykres_statyczny(Figura_wykresu):

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

class Wykres_dynamiczny_1(Figura_wykresu):

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class Wykres_dynamiczny_2(Figura_wykresu):

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.y_var=[random.randint(0, 10) for i in range(10)]
        self.x_var=[i for i in range (10)]
        self.axes.plot(self.x_var,self.y_var, 'r')

    def update_figure(self,data_y):
        
        self.y_var = np.append(self.y_var, data_y )
        self.y_var = self.y_var[1 : ]
        self.axes.cla()
        self.axes.plot(self.x_var, self.y_var, 'r')
        self.draw()
