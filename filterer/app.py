import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from filterer.ui import *


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

        self.setGeometry(0, 0, *window_size)
        self.showMaximized()
        self.setWindowTitle(title)
        self.ui = UI(self)
        self.ui.show_gui()

        btn_select, btn_apply = self.ui.get_buttons()
        btn_select.clicked.connect(self.slot_get_file)
        btn_apply.clicked.connect(self.slot_apply_filter)

    def slot_get_file(self):
        self.input_file, _ = QFileDialog.getOpenFileName(self,
                                                         'Open file',
                                                         './example_images/',
                                                         'Image files (*.jpg *.gif)')
        max_width, max_height = self.ui.get_image_frame_size()

        self.image_pixmap = QPixmap(self.input_file)
        if self.image_pixmap.width() > max_width or self.image_pixmap.height() > max_height:
            if max_width < max_height:
                self.image_pixmap = self.image_pixmap.scaledToWidth(max_width)
            else:
                self.image_pixmap = self.image_pixmap.scaledToHeight(max_height)

        self.ui.get_image_content_label().setPixmap(self.image_pixmap)

    def slot_apply_filter(self):
        self.ui.get_image_content_label().setText("Working...")
