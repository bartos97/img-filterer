from filterer.ui import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageOps, ImageQt


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

        self.input_file = ""
        self.image_pixmap = None
        self.image_pil = None

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
        self.input_file, _ = QFileDialog.getOpenFileName(self,
                                                         'Open file',
                                                         './example_images/',
                                                         'Image files (*.jpg *.gif)')
        if self.input_file:
            self.image_pil = Image.open(self.input_file)
            self.image_pil = ImageOps.grayscale(self.image_pil)
            self.__pil_image_to_pixmap()
            self.__refresh_pixmap()

    def slot_apply_filter(self):
        self.ui.image_frame_content_label.setText("Working...")
        self.image_pil = Image.eval(self.image_pil, lambda x: x/2)
        self.__pil_image_to_pixmap()
        self.__refresh_pixmap()

    def slot_save_file(self):
        msg = QMessageBox()
        try:
            self.image_pil.save("./out.jpg", "JPEG")
            msg.setText("File saved to ./out.jpg")
            msg.setIcon(QMessageBox.Information)
        except IOError:
            msg.setText("Error occured while saving file!")
            msg.setIcon(QMessageBox.Critical)
        finally:
            msg.exec_()

    def __create_pixmap(self, file: str):
        self.image_pixmap = QPixmap(file)
        self.__fix_pixmap_size()
        self.__refresh_pixmap()

    def __pil_image_to_pixmap(self):
        self.image_pixmap = QPixmap(
            QImage(ImageQt.ImageQt(self.image_pil))
        )
        self.__fix_pixmap_size()

    def __fix_pixmap_size(self):
        max_width, max_height = self.ui.get_image_frame_size()

        if self.image_pixmap.width() > max_width or self.image_pixmap.height() > max_height:
            if max_width < max_height:
                self.image_pixmap = self.image_pixmap.scaledToWidth(max_width)
            else:
                self.image_pixmap = self.image_pixmap.scaledToHeight(max_height)

    def __refresh_pixmap(self):
        self.ui.image_frame_content_label.setPixmap(self.image_pixmap)
