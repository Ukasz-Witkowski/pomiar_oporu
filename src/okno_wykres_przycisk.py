from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from wykres import wykres
import random
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

        self.canvas = wykres(self, width=21, height=37, dpi=100)
        self.label =  QtWidgets.QVBoxLayout()
        self.label.setObjectName("label")
        self.label.setGeometry(QtCore.QRect(130, 90, 801, 451))
        self.label.addWidget(self.canvas)
        n_data = 20
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

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
   
    def update_plot(self):
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        self.canvas.draw()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.przycisk1.setText(_translate("MainWindow", "cyk obrazek"))
        self.przycisk2.setText(_translate("MainWindow", "cyk autor"))
        self.napis.setText(_translate("MainWindow", "Obrazek"))
        self.menuPlik.setTitle(_translate("MainWindow", "Plik"))
        self.menuEdytuj.setTitle(_translate("MainWindow", "Edytuj"))
        self.actionNowy.setText(_translate("MainWindow", "Nowy"))
        self.actionNowy.setStatusTip(_translate("MainWindow", "wykonaj nowy pomiar"))
        self.actionNowy.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionZapisz.setText(_translate("MainWindow", "Zapisz"))
        self.actionZapisz.setStatusTip(_translate("MainWindow", "zapisz pomiary"))
        self.actionZapisz.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionKopiuj.setText(_translate("MainWindow", "Kopiuj"))
        self.actionKopiuj.setStatusTip(_translate("MainWindow", "kopiuj dane"))
        self.actionKopiuj.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionWklej.setText(_translate("MainWindow", "Wklej"))
        self.actionWklej.setStatusTip(_translate("MainWindow", "wklej dane"))
        self.actionWklej.setShortcut(_translate("MainWindow", "Ctrl+V"))
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
