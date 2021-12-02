from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(949, 446)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.przycisk1 = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk1.setGeometry(QtCore.QRect(160, 130, 131, 61))
        self.przycisk1.setObjectName("przycisk1")
        
        self.przycisk2 = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk2.setGeometry(QtCore.QRect(160, 200, 131, 61))
        self.przycisk2.setObjectName("przycisk2")
        
        self.napis = QtWidgets.QLabel(self.centralwidget)
        self.napis.setGeometry(QtCore.QRect(390, 50, 131, 51))
        self.napis.setObjectName("napis")
        
        MainWindow.setCentralWidget(self.centralwidget)
       
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 949, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.przycisk1.setText(_translate("MainWindow", "klik 1"))
        self.przycisk2.setText(_translate("MainWindow", "klik 2"))
        self.napis.setText(_translate("MainWindow", "ratatat"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
