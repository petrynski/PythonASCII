import sys
import math
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageDraw, ImageFont, ImageQt


class MainWindow(QMainWindow):
    def __init__(self):
        self.pic = None
        self.scaled_pic = None
        self.gen_im = None
        self.charset = "#$XKb%,-. "
        self.maxImgWidth = 300;
        super(MainWindow, self).__init__()
        loadUi("asciiConverterMainWindow.ui", self)

        self.fileButton.clicked.connect(self.file_open)
        self.GenerateBWButton.clicked.connect(self.generate_bw)

    def file_open(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\', 'Image files (*.jpg *.jpeg *.bmp *.png)')
        self.fileLocationLabel.setText(file_name)
        self.pic = Image.open(file_name)
        self.originalPicture.setPixmap(QPixmap(file_name))

    def generate_bw(self):
        if self.pic:
            text_file = open("Output.txt", "w")
            width, height = self.pic.size
            self.maxImgWidth = int(self.ScaleInput.text())
            scale_factor = self.maxImgWidth / width
            self.scaled_pic = self.pic.resize((int(width*scale_factor), int(height*scale_factor*0.5)), Image.NEAREST)
            pix_map = self.scaled_pic.load()
            width, height = self.scaled_pic.size
            charlist = list(self.charset)
            length = len(charlist)
            interval = length / 256
            for j in range(height):
                for i in range(width):
                    r, g, b = pix_map[i, j]
                    bw = int(r/3 + g/3 + b/3)
                    pix_map[i, j] = (bw, bw, bw)
                    text_file.write(self.charset[math.floor(bw*interval)])
                text_file.write('\n')
            self.gen_im = ImageQt.ImageQt(self.scaled_pic)
            pix = QPixmap.fromImage(self.gen_im)
            self.generatedPicture.setPixmap(pix)


def window():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedWidth(1000)
    widget.setFixedHeight(600)
    widget.show()
    sys.exit(app.exec_())


window()
