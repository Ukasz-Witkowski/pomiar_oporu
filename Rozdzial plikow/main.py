import sys
import szkielet
import funkcje 

if __name__ == "__main__":
    aplikacja = szkielet.QtWidgets.QApplication(sys.argv)
    fun=funkcje.program()
    fun.okno.show()
    sys.exit(aplikacja.exec_())

