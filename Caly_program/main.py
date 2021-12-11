import sys
import szkielet_ok

if __name__ == "__main__":
    aplikacja = szkielet_ok.QtWidgets.QApplication(sys.argv)
    okno = szkielet_ok.QtWidgets.QMainWindow()
    ui = szkielet_ok.Ui_MainWindow()
    ui.setupUi(okno)
    okno.show()
    sys.exit(aplikacja.exec_())

