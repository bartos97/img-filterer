import sys
from PyQt5.QtWidgets import QApplication
from filterer.app import App


if __name__ == '__main__':
    app_instance = QApplication(sys.argv)
    ex = App()
    sys.exit(app_instance.exec_())
