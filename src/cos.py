import sys
import random
import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import squarify

class Widget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        button = QtWidgets.QPushButton("random plot")
        button.clicked.connect(self.plot)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.canvas)
        lay.addWidget(button)
        self.plot()

    def plot(self):
        self.figure.clear()
        df = pd.DataFrame({'nb_people':[random.randint(1, 10) for i in range(4)], 'group':["group A", "group B", "group C", "group D"] })
        ax = self.figure.add_subplot(111)
        squarify.plot(sizes=df['nb_people'], label=df['group'], alpha=.8 ,ax=ax)
        ax.axis('off')
        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())