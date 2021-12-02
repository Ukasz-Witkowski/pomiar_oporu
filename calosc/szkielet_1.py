from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
matplotlib.use('Qt5Agg')        # Make sure that we are using QT5
from PyQt5 import QtCore, QtWidgets
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtGui, QtWidgets

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
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class Wykres_dynamiczny_2(Figura_wykresu):

    def __init__(self, *args, **kwargs):
        Figura_wykresu.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 713)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.przycisk2 = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk2.setGeometry(QtCore.QRect(120, 570, 161, 51))
        self.przycisk2.setObjectName("przycisk2")
        
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(40, 340, 22, 281))
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        
        self.widget_1 = QtWidgets.QWidget(self.centralwidget)
        self.widget_1.setGeometry(QtCore.QRect(70, 30, 311, 281))
        self.widget_1.setObjectName("widget_1")
        
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(410, 30, 311, 281))
        self.widget_2.setObjectName("widget_2")
        
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(410, 340, 311, 281))
        self.widget_3.setObjectName("widget_3")

        self.sc = Wykres_statyczny(self.widget_1, width=2.5, height=2.5, dpi=100)
        self.dc1 = Wykres_dynamiczny_1(self.widget_2, width=2.5, height=2.5, dpi=100)
        self.dc2 = Wykres_dynamiczny_2(self.widget_3, width=2.5, height=2.5, dpi=100)

        self.label_moc_tytul = QtWidgets.QLabel(self.centralwidget)
        self.label_moc_tytul.setGeometry(QtCore.QRect(110, 350, 171, 31))
        
        font = QtGui.QFont()
        font.setPointSize(12)
        
        self.label_moc_tytul.setFont(font)
        self.label_moc_tytul.setAlignment(QtCore.Qt.AlignCenter)
        self.label_moc_tytul.setObjectName("label_moc_tytul")
        
        self.label_moc_wartosc = QtWidgets.QLabel(self.centralwidget)
        self.label_moc_wartosc.setGeometry(QtCore.QRect(110, 410, 171, 31))
        
        font = QtGui.QFont()
        font.setPointSize(12)
        
        self.label_moc_wartosc.setFont(font)
        self.label_moc_wartosc.setAlignment(QtCore.Qt.AlignCenter)
        self.label_moc_wartosc.setObjectName("label_moc_wartosc")
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 26))
        self.menubar.setObjectName("menubar")
        
        self.menupliki = QtWidgets.QMenu(self.menubar)
        self.menupliki.setObjectName("menupliki")
        
        self.menuustawienia = QtWidgets.QMenu(self.menubar)
        self.menuustawienia.setObjectName("menuustawienia")
        
        self.menupomoc = QtWidgets.QMenu(self.menubar)
        self.menupomoc.setObjectName("menupomoc")
        
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        
        MainWindow.setStatusBar(self.statusbar)
        
        self.menubar.addAction(self.menupliki.menuAction())
        self.menubar.addAction(self.menuustawienia.menuAction())
        self.menubar.addAction(self.menupomoc.menuAction())

        self.retranslateUi(MainWindow)
        self.verticalSlider.valueChanged['int'].connect(self.label_moc_wartosc.setNum)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.przycisk2.setText(_translate("MainWindow", "Start"))
        self.przycisk2.clicked.connect(self.dc2.update_figure)
        self.label_moc_tytul.setText(_translate("MainWindow", "Moc grzałki"))
        self.label_moc_wartosc.setText(_translate("MainWindow", "0"))
        self.menupliki.setTitle(_translate("MainWindow", "pliki"))
        self.menuustawienia.setTitle(_translate("MainWindow", "ustawienia"))
        self.menupomoc.setTitle(_translate("MainWindow", "pomoc"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
