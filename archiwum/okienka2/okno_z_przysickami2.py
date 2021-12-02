
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(945, 712)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.przycisk2 = QtWidgets.QPushButton(self.centralwidget)
        self.przycisk2.setGeometry(QtCore.QRect(480, 520, 221, 71))
        self.przycisk2.setObjectName("przycisk2")
       
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(100, 80, 22, 351))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
       
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(260, 70, 401, 341))
        self.widget.setObjectName("widget")
       
        self.przycisk1 = QtWidgets.QPushButton(self.widget)
        self.przycisk1.setGeometry(QtCore.QRect(-40, 50, 181, 71))
        self.przycisk1.setObjectName("przycisk1")
       
        MainWindow.setCentralWidget(self.centralwidget)
       
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 26))
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
        self.przycisk2.setText(_translate("MainWindow", "napis na przyscisku2"))
        self.przycisk1.setText(_translate("MainWindow", "napis na przycisku1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
