import sys
from PyQt5 import QtWidgets
from ui_autoloop import AutoLoopManagerGUI

def main():
    """Точка входа в приложение."""
    app = QtWidgets.QApplication(sys.argv)
    window = AutoLoopManagerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
