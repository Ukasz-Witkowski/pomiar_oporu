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

class Wykres_temp(Figura_wykresu):
    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        self.dane=[[NaN,NaN]]

    def update_figure(self):
        self.axes.cla()
        self.axes.plot(self.dane[:,0], self.dane[:,1], 'r')
        self.draw()

class Wykres_probka(Figura_wykresu):
    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.dane=[[NaN,NaN,NaN]]
        self.axes.plot([],[], 'b')

    def update_figure(self):
        self.axes.cla()
        self.axes.plot(self.dane[:,0], self.dane[:,1], 'b')
        self.draw()

class Wykres_20kanal(Figura_wykresu):
    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.dane=[[NaN,NaN]]
        self.axes.plot([],[], 'b')

    def update_figure(self):
        self.axes.cla()
        self.axes.plot(self.dane[:,0], self.dane[:,1], 'b')
        self.draw()
