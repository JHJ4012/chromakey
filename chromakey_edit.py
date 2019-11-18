from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class EditWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.initUI()

    def initUI(self):

        self.setFixedSize(1400, 800)
        self.setWindowTitle('chroma key edit')

        self.img1 = QImage("image/background2.jpg").scaled(600,400)
        self.img2 = QImage("image/background2.jpg").scaled(600,400)

        self.for_file_btn1 = QPushButton('불러오기', self)
        self.for_file_btn1.setGeometry(550,460,100,50)
        self.for_file_btn1.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_file_btn1.clicked.connect(lambda state, button = self.for_file_btn1 : self.openFile(state, button))

        self.for_file_btn2 = QPushButton('불러오기', self)
        self.for_file_btn2.setGeometry(1250,460, 100,50)
        self.for_file_btn2.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_file_btn2.clicked.connect(lambda state, button = self.for_file_btn2 : self.openFile(state, button))

        self.for_webcam1 = QPushButton('촬영', self)
        self.for_webcam1.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_webcam1.setGeometry(440,460,100,50)

        self.for_webcam2 = QPushButton('촬영', self)
        self.for_webcam2.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_webcam2.setGeometry(1140,460,100,50)

        self.select_color_btn = QPushButton('색', self)
        self.select_color_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_color_btn.setGeometry(50, 460, 100, 50)

        self.test_label1 = QLabel(self)
        self.test_label1.setGeometry(50, 520, 600, 200)
        self.test_label1.setStyleSheet("background-color : red")

        self.test_label2 = QLabel(self)
        self.test_label2.setGeometry(750, 520, 600, 200)
        self.test_label2.setStyleSheet("background-color : red")

        self.back_first_window = QPushButton('처음으로', self)
        self.back_first_window.setGeometry(50, 730, 100, 50)
        self.back_first_window.setCursor(QCursor(Qt.PointingHandCursor))
        # self.back_first_window.clicked.connect(self.goToFirst)

        self.complete_btn = QPushButton('완료', self)
        self.complete_btn.setGeometry(1250,730,100,50)
        self.complete_btn.setCursor(QCursor(Qt.PointingHandCursor))
        # self.complete_btn.clicked.connect(self.goToPreview)

    def openFile(self, state, button):
        fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "All Files (*);; Python files (*.py)")

        if fileName:
            print(fileName)
            if button == self.for_file_btn1:
                self.img1 = QImage(fileName).scaled(600,400)
            elif button == self.for_file_btn2:
                self.img2 = QImage(fileName).scaled(600,400)

    def drawImages(self, painter):
        painter.drawImage(50, 50, self.img1)
        painter.drawImage(750, 50, self.img2)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.drawImages(painter)
        painter.end()

    # def goToPreview(self):
    #     self.preview_window = chromakey_preview.PreviewWindow()
    #     self.hide()
    #     self.preview_window.show()

    # def goToFirst(self):
    #     self.first_window = chromakey_first.MainWindow()
    #     self.close()
    #     self.first_window.show()
