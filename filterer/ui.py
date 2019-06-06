from PyQt5.QtWidgets import (
    QGridLayout, QHBoxLayout, QVBoxLayout, QGroupBox,
    QPushButton, QLineEdit, QLabel,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

from filterer.exceptions import *


class UI:
    def __init__(self, window_ptr):
        self.__options = {
            'GRID_GUTTER': 15,
            "INPUTS_WIDTH": 3,
        }

        self.__image_frame = None
        self.__image_frame_content_label = None
        self.__footer_btns = []
        self.__kernel_matrix = []

        self.__window_ptr = window_ptr
        self.__main_grid = QVBoxLayout()

        self.__init_img_frame("Image")
        self.__init_filter_grid("Kernel convolution matrix")
        self.__init_footer_buttons(("Select image", "Apply filter", "Save"))

    def get_buttons(self):
        return self.__footer_btns

    def get_input_values(self):
        vals = []
        for i, row in enumerate(self.__kernel_matrix):
            for j, input_elem in enumerate(row):
                data = input_elem.text()
                if len(data):
                    vals.append(float(data))
                else:
                    raise EmptyFieldError("You must fill all the inputs in kernel!")
                    # vals.append(1.0)
        return vals

    def get_image_content_label(self):
        return self.__image_frame_content_label

    def get_image_frame_size(self):
        return (
            self.__image_frame_content_label.geometry().width(),
            self.__image_frame_content_label.geometry().height()
        )

    def show_gui(self):
        self.__window_ptr.setLayout(self.__main_grid)
        self.__window_ptr.show()

    def __init_img_frame(self, title: str):
        self.__image_frame_content_label = QLabel()
        self.__image_frame_content_label.setAlignment(Qt.AlignCenter)
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.__image_frame_content_label)

        self.__image_frame = QGroupBox(title)
        self.__image_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__image_frame.setLayout(image_layout)

        local_layout = QVBoxLayout()
        local_layout.setAlignment(Qt.AlignTop)
        local_layout.addWidget(self.__image_frame)

        self.__main_grid.addLayout(local_layout)

    def __init_filter_grid(self, title: str):
        local_layout = QVBoxLayout()
        local_layout.setAlignment(Qt.AlignBottom)
        frame = QGroupBox(title)
        grid = QGridLayout()

        # Regular expresion that will allow to input only int or float (dot seperated)
        regex = QRegExp(r"[-+]?\d*\.\d+|\d+")

        self.__kernel_matrix = [
            [QLineEdit() for _ in range(self.__options['INPUTS_WIDTH'])]
            for _ in range(self.__options['INPUTS_WIDTH'])
        ]
        for i, row in enumerate(self.__kernel_matrix):
            for j, input_elem in enumerate(row):
                input_elem.setValidator(QRegExpValidator(regex))
                grid.addWidget(input_elem, i, j)

        frame.setLayout(grid)
        local_layout.addWidget(frame)
        self.__main_grid.addLayout(local_layout)

    def __init_footer_buttons(self, titles: tuple):
        local_layout = QHBoxLayout()
        local_layout.setContentsMargins(0, self.__options['GRID_GUTTER'], 0, 0)

        for title in titles:
            tmp_btn = QPushButton(title)
            self.__footer_btns.append(tmp_btn)
            local_layout.addWidget(tmp_btn)

        self.__main_grid.addLayout(local_layout)
