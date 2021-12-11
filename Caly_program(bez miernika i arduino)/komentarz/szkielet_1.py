import sys
import matplotlib
matplotlib.use('Qt5Agg')        # używamy QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
import wykres
import grzalka
import miernik

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 713)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.przycisk_start = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk_start.setGeometry(QtCore.QRect(120, 570, 161, 51))
        self.przycisk_start.setObjectName("przycisk_start")
        
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(40, 340, 22, 281))
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        
        self.widget_1 = QtWidgets.QWidget(self.centralwidget)
        self.widget_1.setGeometry(QtCore.QRect(100, 30, 300, 300))
        self.widget_1.setObjectName("widget_1")
        
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(410, 30, 300, 300))
        self.widget_2.setObjectName("widget_2")
        
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(410, 340, 300, 300))
        self.widget_3.setObjectName("widget_3")

        self.sc = wykres.Wykres_statyczny(self.widget_1, width=6, height=6, dpi=50)
        self.dc1 = wykres.Wykres_dynamiczny_1(self.widget_2, width=3, height=3, dpi=100)
        self.dc2 = wykres.Wykres_dynamiczny_2(self.widget_3, width=3, height=3, dpi=100)

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

        self.moc=0

        self.arduino=grzalka.Grzanie()
        self.miernik=miernik.Aparature()
        # self.miernik.ustaw_r
        # self.miernik.zamknij(13)

        self.retranslateUi(MainWindow)
        self.verticalSlider.valueChanged['int'].connect(self.label_moc_wartosc.setNum)
        self.verticalSlider.valueChanged['int'].connect(self.zmiana1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.przycisk_start.setText(_translate("MainWindow", "Start"))
        # self.przycisk_start.clicked.connect(self.dc2.update_figure(5.43))
        self.przycisk_start.clicked.connect(self.zmiana2)
        self.label_moc_tytul.setText(_translate("MainWindow", "Moc grzałki"))
        self.label_moc_wartosc.setText(_translate("MainWindow", "0"))
        self.menupliki.setTitle(_translate("MainWindow", "pliki"))
        self.menuustawienia.setTitle(_translate("MainWindow", "ustawienia"))
        self.menupomoc.setTitle(_translate("MainWindow", "pomoc"))

    def zmiana1(self,w):
        self.moc=w

    def zmiana2(self):
        self.arduino.zmien_moc(self.moc)

