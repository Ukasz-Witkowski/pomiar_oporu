from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Fig_Can
import sys
import numpy as np
import time


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


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.przycisk1 = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk1.setGeometry(QtCore.QRect(140, 590, 131, 61))
        self.przycisk1.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.przycisk1.setObjectName("przycisk1")

        self.przycisk2 = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk2.setGeometry(QtCore.QRect(660, 590, 131, 61))
        self.przycisk2.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.przycisk2.setObjectName("przycisk2")

        self.napis = QtWidgets.QLabel(self.centralwidget)
        self.napis.setGeometry(QtCore.QRect(330, 10, 301, 71))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.napis.setFont(font)
        self.napis.setAlignment(QtCore.Qt.AlignCenter)
        self.napis.setObjectName("napis")

        # self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setGeometry(QtCore.QRect(130, 90, 801, 451))
        # self.label.setText("")
        # self.label.setPixmap(QtGui.QPixmap("imgs/obrazek.png"))
        # self.label.setScaledContents(True)
        self.label = wykres(self)
        # self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1037, 26))
        self.menubar.setObjectName("menubar")

        self.menuPlik = QtWidgets.QMenu(self.menubar)
        self.menuPlik.setObjectName("menuPlik")

        self.menuEdytuj = QtWidgets.QMenu(self.menubar)
        self.menuEdytuj.setObjectName("menuEdytuj")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionNowy = QtWidgets.QAction(MainWindow)
        self.actionNowy.setObjectName("actionNowy")

        self.actionZapisz = QtWidgets.QAction(MainWindow)
        self.actionZapisz.setObjectName("actionZapisz")

        self.actionKopiuj = QtWidgets.QAction(MainWindow)
        self.actionKopiuj.setObjectName("actionKopiuj")

        self.actionWklej = QtWidgets.QAction(MainWindow)
        self.actionWklej.setObjectName("actionWklej")

        self.menuPlik.addAction(self.actionNowy)
        self.menuPlik.addAction(self.actionZapisz)

        self.menuEdytuj.addAction(self.actionKopiuj)
        self.menuEdytuj.addAction(self.actionWklej)

        self.menubar.addAction(self.menuPlik.menuAction())
        self.menubar.addAction(self.menuEdytuj.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.przycisk1.setText(_translate("MainWindow", "cyk obrazek"))
        self.przycisk2.setText(_translate("MainWindow", "cyk autor"))
        self.napis.setText(_translate("MainWindow", "Obrazek"))
        self.menuPlik.setTitle(_translate("MainWindow", "Plik"))
        self.menuEdytuj.setTitle(_translate("MainWindow", "Edytuj"))
        self.actionNowy.setText(_translate("MainWindow", "Nowy"))
        self.actionNowy.setStatusTip(_translate(
            "MainWindow", "wykonaj nowy pomiar"))
        self.actionNowy.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionZapisz.setText(_translate("MainWindow", "Zapisz"))
        self.actionZapisz.setStatusTip(
            _translate("MainWindow", "zapisz pomiary"))
        self.actionZapisz.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionKopiuj.setText(_translate("MainWindow", "Kopiuj"))
        self.actionKopiuj.setStatusTip(_translate("MainWindow", "kopiuj dane"))
        self.actionKopiuj.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionWklej.setText(_translate("MainWindow", "Wklej"))
        self.actionWklej.setStatusTip(_translate("MainWindow", "wklej dane"))
        self.actionWklej.setShortcut(_translate("MainWindow", "Ctrl+V"))

        self.przycisk1.clicked.connect(self.poka_obrazek)
        self.przycisk2.clicked.connect(self.poka_kakunie)

    def poka_obrazek(self):
     # self.label.setPixmap(QtGui.QPixmap("imgs/obrazek.png"))
        self.napis.setText("Obrazek")

    def poka_kakunie(self):
        self.label.setPixmap(QtGui.QPixmap("imgs/autor.png"))
        self.napis.setText("Kakunia")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
