from PyQt5.QtWidgets import QWidget


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Python image filterer by Bartłomiej Zając'
        self.left = 0
        self.top = 50
        self.width = 640
        self.height = 480
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
