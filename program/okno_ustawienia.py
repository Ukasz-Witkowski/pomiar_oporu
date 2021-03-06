from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(664, 230)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 221, 20))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(290, 30, 291, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(290, 70, 291, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 221, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 110, 221, 20))
        self.label_3.setObjectName("label_3")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(290, 110, 81, 20))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(490, 170, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 180, 391, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ustawienia"))
        self.label.setText(_translate("Dialog", "Ściażka zapisu plików wyjściowych*:"))
        self.lineEdit.setText(_translate("Dialog", "C:\\\\Users\\\\Praca\\\\Desktop\\\\pomiary\\\\"))
        self.lineEdit_2.setText(_translate("Dialog", "test.csv"))
        self.label_2.setText(_translate("Dialog", "Domyślna nazwa pliku wyjściowego:"))
        self.label_3.setText(_translate("Dialog", "Zapis do pliku wyjściowego"))
        self.pushButton.setText(_translate("Dialog", "Zatwierdź"))
        self.label_4.setText(_translate("Dialog", "*przy zapisie ścieżki używaj podwójnych ukośników  \"\\\\\""))

