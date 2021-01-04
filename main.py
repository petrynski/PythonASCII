import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("asciiConverterMainWindow.ui", self)

        self.fileButton.clicked.connect(self.file_open)

    def file_open(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C:\\', 'Image files (*.jpg *.jpeg *.bmp *.png)')
        self.fileLocationLabel.setText(file_name)
        self.originalPicture.setPixmap(QPixmap(file_name))


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
