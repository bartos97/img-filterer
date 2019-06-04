from PyQt5.QtWidgets import (
    QGridLayout, QHBoxLayout, QVBoxLayout, QGroupBox,
    QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator


class UI:
    def __init__(self, window_ptr):
        self.options = {
            'GRID_GUTTER': 15
        }

        self.window_ptr = window_ptr
        self.main_vgrid = None
        self.footer_btns = []
        self.kernel_matrix = []

        self.init_main_grid()
        self.init_photo_frame("Image")
        self.init_filter_grid("Kernel convolution matrix")
        self.init_footer_buttons(("Select image", "Apply filter"))

    def show_gui(self):
        self.window_ptr.setLayout(self.main_vgrid)
        self.window_ptr.show()

    def get_buttons(self):
        return self.footer_btns

    def get_inputs(self):
        return self.kernel_matrix

    def init_main_grid(self):
        self.main_vgrid = QVBoxLayout()

    def init_photo_frame(self, title: str):
        local_layout = QVBoxLayout()
        local_layout.setAlignment(Qt.AlignTop)
        frame = QGroupBox(title)
        local_layout.addWidget(frame)
        self.main_vgrid.addLayout(local_layout)

    def init_filter_grid(self, title: str):
        local_layout = QVBoxLayout()
        local_layout.setAlignment(Qt.AlignBottom)
        frame = QGroupBox(title)
        grid = QGridLayout()

        # Regular expresion that will allow to input only int or float
        regex = QRegExp("(\d+(?:\.\d+)?)")

        self.kernel_matrix = [[QLineEdit() for _ in range(3)] for _ in range(3)]
        for i, row in enumerate(self.kernel_matrix):
            for j, input_elem in enumerate(row):
                input_elem.setValidator(QRegExpValidator(regex))
                grid.addWidget(input_elem, i, j)

        frame.setLayout(grid)
        local_layout.addWidget(frame)
        self.main_vgrid.addLayout(local_layout)

    def init_footer_buttons(self, titles: tuple):
        local_layout = QHBoxLayout()
        local_layout.setContentsMargins(0, self.options['GRID_GUTTER'], 0, 0)

        for title in titles:
            tmp_btn = QPushButton(title)
            self.footer_btns.append(tmp_btn)
            local_layout.addWidget(tmp_btn)

        self.main_vgrid.addLayout(local_layout)
