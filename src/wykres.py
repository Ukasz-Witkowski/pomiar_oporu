import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Fig_Can


class wykres(Fig_Can):  # dziedziczy po klasie bedącej w jakiejś bibliotece matplotlib
    def __init__(self, parent):

        self.fig, self.ax = plt.subplots()

        super().__init__(self.fig)
        self.setParent(parent)

        self.X = np.arange(0.0, 2.0, 0.01)
        self.Y = 1 + np.sin(2 * np.pi * self.X)

        self.line, = self.ax.plot(self.X, self.Y)
        self.ax.set(xlabel='Czas[s]', ylabel='Napięcie[mV]',
                    title='Opis tego co mierzymy')
