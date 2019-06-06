import sys

from filterer.ui import *
import filterer.dll_utils as dll

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageOps, ImageQt

import numpy as np


class App(QWidget):
    app_instance = None
    self_instance = None

    @staticmethod
    def run(title: str, window_size: tuple):
        App.app_instance = QApplication(sys.argv)
        App.instance = App(title, window_size)
        sys.exit(App.app_instance.exec_())

    def __init__(self, title: str, window_size: tuple):
        super().__init__()

        self.__lib = dll.Lib('./img-lib/lib/img-lib')

        self.__input_file = ""
        self.__image_pixmap = None
        self.__image_pil = None

        self.setGeometry(0, 0, *window_size)
        self.showMaximized()
        self.setWindowTitle(title)
        self.ui = UI(self)
        self.ui.show_gui()

        btn_select, btn_apply, btn_save = self.ui.get_buttons()
        btn_select.clicked.connect(self.slot_get_file)
        btn_apply.clicked.connect(self.slot_apply_filter)
        btn_save.clicked.connect(self.slot_save_file)

    def slot_get_file(self):
        self.__input_file, _ = QFileDialog.getOpenFileName(self,
                                                           'Open file',
                                                           './example_images/',
                                                           'Image files (*.jpg *.gif *.png *.bmp)')
        if self.__input_file:
            self.__image_pil = Image.open(self.__input_file)
            self.__image_pil = ImageOps.grayscale(self.__image_pil)
            self.__pil_image_to_pixmap()
            self.__refresh_pixmap()

    def slot_apply_filter(self):
        if not self.__image_pil:
            self.ui.get_image_content_label().setText("Select image first!")
            return None

        image_data = np.array(self.__image_pil)
        try:
            kernel = np.array(self.ui.get_input_values(), dtype=np.float32)
        except FiltererException as e:
            msg = QMessageBox()
            msg.setText(e.message)
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return None

        self.__lib.filter_kernel_conv(image_data, self.__image_pil.width, kernel)
        self.__image_pil = Image.fromarray(image_data)

        self.__pil_image_to_pixmap()
        self.__refresh_pixmap()

    def slot_save_file(self):
        if not self.__image_pil:
            self.ui.get_image_content_label().setText("Select image first!")
            return None

        msg = QMessageBox()
        try:
            self.__image_pil.save("./out.jpg", "JPEG")
            msg.setText("File saved to ./out.jpg")
            msg.setIcon(QMessageBox.Information)
        except IOError:
            msg.setText("Error occured while saving file!")
            msg.setIcon(QMessageBox.Critical)
        finally:
            msg.exec_()

    def __create_pixmap(self, file: str):
        self.__image_pixmap = QPixmap(file)
        self.__fix_pixmap_size()
        self.__refresh_pixmap()

    def __pil_image_to_pixmap(self):
        self.__image_pixmap = QPixmap(
            QImage(ImageQt.ImageQt(self.__image_pil))
        )
        self.__fix_pixmap_size()

    def __fix_pixmap_size(self):
        max_width, max_height = self.ui.get_image_frame_size()

        if self.__image_pixmap.width() > max_width or self.__image_pixmap.height() > max_height:
            if max_width < max_height:
                self.__image_pixmap = self.__image_pixmap.scaledToWidth(max_width)
            else:
                self.__image_pixmap = self.__image_pixmap.scaledToHeight(max_height)

    def __refresh_pixmap(self):
        self.ui.get_image_content_label().setPixmap(self.__image_pixmap)
