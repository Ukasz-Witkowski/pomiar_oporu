from sys import dllhandle
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import NaN, arange, sin, pi
import numpy as np


class Figura_wykresu(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
    def compute_initial_figure(self):
        pass

class Wykres_temp(Figura_wykresu):
    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        self.dane=[[NaN,NaN]]
        self.axes.set_ylabel('Temperatura [K]')
        self.axes.set_xlabel('Czas [s]')
        self.fig.set_tight_layout(True)

    def update_figure(self):
        self.axes.cla()
        self.axes.set_ylabel('Temperatura [K]')
        self.axes.set_xlabel('Czas [s]')
        self.axes.plot(self.dane[:,0], self.dane[:,1], 'r')
        self.draw()

    def reset_wykres(self):
        self.dane=[[NaN,NaN]]
        self.axes.cla()
        self.axes.set_ylabel('Temperatura [K]')
        self.axes.set_xlabel('Czas [s]')
        self.fig.set_tight_layout(True)
        self.draw()

class Wykres_probka(Figura_wykresu):
    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        self.dane=[[NaN,NaN,NaN]]
        self.axes.set_ylabel('Opór [Ohm]')
        self.axes.set_xlabel('Czas [s]')
        self.fig.set_tight_layout(True)
        self.time_temp=0

    def zmien_osx(self,t):
        self.time_temp=t
        if(np.size(self.dane)>3):
            self.update_figure()
        if(self.time_temp==0):
            self.axes.set_xlabel('Czas [s]')
        if(self.time_temp==1):
            self.axes.set_xlabel('Temperatura [K]')
        self.draw()

    def reset_wykres(self):
        self.dane=[[NaN,NaN,NaN]]
        self.time_temp=0
        self.axes.cla()
        self.axes.set_ylabel('Opór [Ohm]')
        self.axes.set_xlabel('Czas [s]')
        self.fig.set_tight_layout(True)
        self.draw()
        
    def update_figure(self):
        self.axes.cla()
        self.axes.set_ylabel('Opór [Ohm]')
        if(self.time_temp==0):
            self.axes.plot(self.dane[:,0], self.dane[:,2], 'b')
            self.axes.set_xlabel('Czas [s]')
        if(self.time_temp==1):
            self.axes.plot(self.dane[:,1], self.dane[:,2], 'b')
            self.axes.set_xlabel('Temperatura [K]')
        self.draw()


class Wykres_20kanal(Figura_wykresu):
    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)
        self.tryb=[[0 for x in range(20)],[0 for x in range(20)]]
        self.dane=[[NaN for x in range(40)]]
        self.axes2=self.axes.twinx()
        self.axes.set_xlabel('Czas [s]')
        self.axes.set_ylabel('Opór [Ohm]',color="blue")
        self.axes2.set_ylabel('Napięcie [V]',color="red")
        self.fig.set_tight_layout(True)

    def update_figure(self):
        self.axes.cla()
        self.axes2.cla()
        self.axes.set_xlabel('Czas [s]')
        self.axes.set_ylabel('Opór [Ohm]',color="blue")
        self.axes2.set_ylabel('Napięcie [V]',color="red")
        for i in range(20):
            if(self.tryb[0][i]==1):
                if(self.tryb[1][i]==0):
                    self.axes.plot(self.dane[:,i*2], self.dane[:,i*2-1], 'r',label=str(i))    
                    self.axes.text(self.dane[:,i*2][-1], self.dane[:,i*2-1][-1], str(i+1))
                if(self.tryb[1][i]==1):
                    self.axes2.plot(self.dane[:,i*2], self.dane[:,i*2-1], 'b',label=str(i))
                    self.axes2.text(self.dane[:,i*2][-1], self.dane[:,i*2-1][-1], str(i+1))
        self.draw()

    def reset_wykres(self):
        self.dane=[[NaN for x in range(40)]]
        self.axes.cla()
        self.axes2.cla()
        self.axes.set_xlabel('Czas [s]')
        self.axes.set_ylabel('Opór [Ohm]',color="blue")
        self.axes2.set_ylabel('Napięcie [V]',color="red")
        self.fig.set_tight_layout(True)
        self.draw()
