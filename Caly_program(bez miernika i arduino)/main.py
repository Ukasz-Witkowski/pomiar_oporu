import sys
import szkielet

if __name__ == "__main__":
    aplikacja = szkielet.QtWidgets.QApplication(sys.argv)
    okno = szkielet.QtWidgets.QMainWindow()
    ui = szkielet.Ui_MainWindow()
    ui.setupUi(okno)
    okno.show()
    sys.exit(aplikacja.exec_())

