import sys
import math
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw, ImageFont, ImageQt


class MainWindow(QMainWindow):
    def __init__(self):
        self.pic = None
        self.scaled_pic = None
        self.gen_im = None
        self.image_string = ""
        self.maxImgWidth = 300
        self.preview_image = None
        self.charset = ""
        super(MainWindow, self).__init__()
        loadUi("asciiConverterMainWindow.ui", self)

        self.fileButton.clicked.connect(self.file_open)
        self.confirmCharSetButton.clicked.connect(self.get_charset)
        self.GenerateBWButton.clicked.connect(self.generate_bw)
        self.GenerateColourButton.clicked.connect(self.generate_rgb)
        self.SaveAsImgButton.clicked.connect(self.save_as_image)
        self.SaveAsTxtButton.clicked.connect(self.save_as_text)
        self.change_charset("#$8SXbhoni,-. ")

    def get_charset(self):
        txt = self.charSetInput.text()
        if txt:
            self.change_charset(txt)

    def generate_bw(self):
        self.generate_ascii_pic(False)

    def generate_rgb(self):
        self.generate_ascii_pic(True)

    def save_as_text(self):
        if self.image_string:
            name, ok = QFileDialog.getSaveFileName(self, 'Save File', 'Txt file (*.txt)')
            if ok:
                file = open(name, 'w')
                file.write(self.image_string)
                file.close()

    def save_as_image(self):
        if self.preview_image:
            name, ok = QFileDialog.getSaveFileName(self, 'Save File', 'Image file (*.jpg *.jpeg *.bmp *.png)')
            if ok:
                self.preview_image.save(name)

    def file_open(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\', )
        if file_name:
            self.fileLocationLabel.setText(file_name)
            self.pic = Image.open(file_name)
            self.originalPicture.setPixmap(QPixmap(file_name))

    def generate_ascii_pic(self, is_color):
        if self.pic:
            self.maxImgWidth = int(self.ScaleInput.text())
            if self.maxImgWidth > 500 or self.maxImgWidth <= 0:
                self.label_7.setStyleSheet("background-color: black; color: red")
                return
            self.label_7.setStyleSheet("background-color default: black; color: black")
            self.image_string = ""
            width, height = self.pic.size
            scale_factor = self.maxImgWidth / width
            self.scaled_pic = self.pic.resize((int(width*scale_factor), int(height*scale_factor*0.5)), Image.NEAREST)
            pix_map = self.scaled_pic.load()
            width, height = self.scaled_pic.size
            if self.DarkModeButton.isChecked():
                self.preview_image = Image.new('RGB', (width * 7, height * 14), color=(0, 0, 0))
                font_color = (255, 255, 255)
                used_charset = self.charset[::-1]
            else:
                self.preview_image = Image.new('RGB', (width * 7, height * 14), color=(255, 255, 255))
                font_color = (0, 0, 0)
                used_charset = self.charset
            d = ImageDraw.Draw(self.preview_image)
            font = ImageFont.truetype('cour.ttf', 12)
            interval = len(self.charset) / 256
            if is_color:
                for j in range(height):
                    for i in range(width):
                        r, g, b = pix_map[i, j]
                        bw = int(r/3 + g/3 + b/3)
                        self.image_string += used_charset[math.floor(bw*interval)]
                        d.text((i*7, 14*j), used_charset[math.floor(bw*interval)], font=font, fill=(r, g, b))
                    self.image_string += '\n'
            else:
                for j in range(height):
                    for i in range(width):
                        r, g, b = pix_map[i, j]
                        bw = int(r/3 + g/3 + b/3)
                        self.image_string += used_charset[math.floor(bw*interval)]
                        d.text((i*7, 14*j), used_charset[math.floor(bw*interval)], font=font, fill=font_color)
                    self.image_string += '\n'
            self.gen_im = ImageQt.ImageQt(self.preview_image)
            pix = QPixmap.fromImage(self.gen_im)
            self.generatedPicture.setPixmap(pix)

    def change_charset(self, txt):
        self.charset = txt
        self.ActiveCharSetLabel.setText("Obecny zestaw znaków: " + '"' + txt + '"')


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
