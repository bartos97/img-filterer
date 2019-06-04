from PyQt5.QtWidgets import QWidget
from filterer.ui import *


class App(QWidget):
    def __init__(self, title: str, start_position: tuple, window_size: tuple):
        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(*start_position, *window_size)
        self.ui = UI(self)
        self.ui.show_gui()

        self.input_file = ""
