import sys
import interfejs
import program

if __name__ == "__main__":
    aplikacja = interfejs.QtWidgets.QApplication(sys.argv)
    fun=program.program()
    fun.okno.show()
    sys.exit(aplikacja.exec_())

