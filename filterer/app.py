from PyQt5.QtWidgets import (
    QGridLayout, QHBoxLayout, QVBoxLayout, QGroupBox,
    QWidget, QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt


class App(QWidget):
    def __init__(self, start_position: tuple, window_size: tuple):
        super().__init__()
        self.title = 'Python image filterer by Bartłomiej Zając'
        self.left, self.top = start_position
        self.width, self.height = window_size
        self.main_vgrid = None
        self.grid_gutter = 15
        self.init_ui()

    def init_ui(self):
        self.init_window()
        self.init_main_grid()
        self.init_photo_frame()
        self.init_filter_grid()
        self.init_buttons()
        self.show_layout()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def init_main_grid(self):
        self.main_vgrid = QVBoxLayout()

    def init_photo_frame(self):
        local_layout = QVBoxLayout()
        local_layout.setAlignment(Qt.AlignTop)
        frame = QGroupBox("Obraz")
        local_layout.addWidget(frame)
        self.main_vgrid.addLayout(local_layout)

    def init_filter_grid(self):
        local_layout = QVBoxLayout()
        local_layout.setAlignment(Qt.AlignBottom)
        frame = QGroupBox("Maska")
        grid = QGridLayout()

        positions = [(i, j) for i in range(3) for j in range(3)]
        for pos in positions:
            grid.addWidget(QLineEdit(), *pos)

        frame.setLayout(grid)
        local_layout.addWidget(frame)
        self.main_vgrid.addLayout(local_layout)

    def init_buttons(self):
        local_layout = QHBoxLayout()
        local_layout.setContentsMargins(0, self.grid_gutter, 0, 0)
        local_layout.addWidget(QPushButton("Dodaj plik"))
        local_layout.addWidget(QPushButton("Filtruj"))
        self.main_vgrid.addLayout(local_layout)

    def show_layout(self):
        self.setLayout(self.main_vgrid)
        self.show()
