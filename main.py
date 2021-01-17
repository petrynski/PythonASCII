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
        super(MainWindow, self).__init__()
        loadUi("asciiConverterMainWindow.ui", self)

        self.fileButton.clicked.connect(self.file_open)
        self.confirmCharSetButton.clicked.connect(self.get_charset)
        self.GenerateBWButton.clicked.connect(self.generate_bw)
        self.GenerateColourButton.clicked.connect(self.generate_rgb)
        self.SaveAsImgButton.clicked.connect(self.save_as_image)
        self.SaveAsTxtButton.clicked.connect(self.save_as_text)
        self.changeCharset("#$8SXbhoni,-. ")

    def get_charset(self):
        txt = self.charSetInput.text()
        print(txt)
        if txt:
            self.changeCharset(txt)

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
            width, height = self.pic.size
            self.maxImgWidth = int(self.ScaleInput.text())
            if self.maxImgWidth > 500 or self.maxImgWidth < -1:
                self.label_7.setStyleSheet("background-color: black; color: red")
                return
            self.image_string = ""
            self.label_7.setStyleSheet("background-color default: black; color: black")
            scale_factor = self.maxImgWidth / width
            self.scaled_pic = self.pic.resize((int(width*scale_factor), int(height*scale_factor*0.5)), Image.NEAREST)
            pix_map = self.scaled_pic.load()
            width, height = self.scaled_pic.size
            if self.DarkModeButton.isChecked():
                self.preview_image = Image.new('RGB', (width * 7, height * 14), color=(0, 0, 0))
                fontColor = (255, 255, 255)
                usedCharset = self.charset[::-1]
            else:
                self.preview_image = Image.new('RGB', (width * 7, height * 14), color=(255, 255, 255))
                fontColor = (0, 0, 0)
                usedCharset = self.charset
            d = ImageDraw.Draw(self.preview_image)
            fnt = ImageFont.truetype('cour.ttf', 12)
            charlist = list(self.charset)
            length = len(charlist)
            interval = length / 256
            if is_color:
                for j in range(height):
                    for i in range(width):
                        r, g, b = pix_map[i, j]
                        bw = int(r/3 + g/3 + b/3)
                        self.image_string += usedCharset[math.floor(bw*interval)]
                        d.text((i*7, 14*j), usedCharset[math.floor(bw*interval)], font=fnt, fill=(r, g, b))
                    self.image_string += '\n'
            else:
                for j in range(height):
                    for i in range(width):
                        r, g, b = pix_map[i, j]
                        bw = int(r/3 + g/3 + b/3)
                        self.image_string += usedCharset[math.floor(bw*interval)]
                        d.text((i*7, 14*j), usedCharset[math.floor(bw*interval)], font=fnt, fill=fontColor)
                    self.image_string += '\n'

            self.gen_im = ImageQt.ImageQt(self.preview_image)
            pix = QPixmap.fromImage(self.gen_im)
            self.generatedPicture.setPixmap(pix)

    def changeCharset(self, txt):
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
