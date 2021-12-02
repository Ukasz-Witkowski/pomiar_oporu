import sys
import szkielet_1

if __name__ == "__main__":
    aplikacja = szkielet_1.QtWidgets.QApplication(sys.argv)
    okno = szkielet_1.QtWidgets.QMainWindow()
    ui = szkielet_1.Ui_MainWindow()
    ui.setupUi(okno)
    okno.show()
    sys.exit(aplikacja.exec_())

