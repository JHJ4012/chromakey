from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2

class EditWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1400,800)

        self.group_box1 = QGroupBox(self)
        self.group_box1.setGeometry(250,10, 200, 40)
        self.group_box1.setStyleSheet("border : None")
        self.group_box2 = QGroupBox(self)
        self.group_box2.setGeometry(950,10, 200, 40)
        self.group_box2.setStyleSheet("border : None")

        self.box_layout1 = QHBoxLayout()
        self.box_layout2 = QHBoxLayout()

        self.group_box1.setLayout(self.box_layout1)
        self.group_box2.setLayout(self.box_layout2)


        self.radio1_photo = QRadioButton("사진")
        self.radio1_video = QRadioButton("동영상")
        self.radio1_photo.setChecked(True)
        self.box_layout1.addWidget(self.radio1_photo)
        self.box_layout1.addWidget(self.radio1_video)

        self.radio2_photo = QRadioButton("사진")
        self.radio2_video = QRadioButton("동영상")
        self.radio2_photo.setChecked(True)
        self.box_layout2.addWidget(self.radio2_photo)
        self.box_layout2.addWidget(self.radio2_video)


        self.img1 = QImage("/").scaled(600,400)
        self.img2 = QImage("/").scaled(600,400)

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

        self.complete_btn = QPushButton('완료', self)
        self.complete_btn.setGeometry(1250,730,100,50)
        self.complete_btn.setCursor(QCursor(Qt.PointingHandCursor))

    # def openFile(self, state, button):
    #     fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "All Files (*);; Python files (*.py)")
    #
    #     if fileName:
    #         print(fileName)
    #         if button == self.for_file_btn1:
    #             self.img1 = QImage(fileName).scaled(600,400)
    #         elif button == self.for_file_btn2:
    #             self.img2 = QImage(fileName).scaled(600,400)

    #opencv를 이용해 화질을 더 좋게 변경
    def openFile(self, state, button):
        fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "All Files (*);; Python files (*.py)")

        if fileName:
            print(fileName)
            if button == self.for_file_btn1:
                self.for_cvImage1 = cv2.imread(fileName)                    #opencv로 파일 불러옴
                self.cvImage1 = cv2.resize(self.for_cvImage1, (600,400))    #불러온 파일 resize
                height, width, byteValue = self.cvImage1.shape              #불러온 파일 정보 변수에 담기
                byteValue = byteValue * width
                cv2.cvtColor(self.cvImage1, cv2.COLOR_BGR2RGB, self.cvImage1)   #BGR을 RGB로 바꾸기

                self.img1 = QImage(self.cvImage1, width, height, byteValue, QImage.Format_RGB888)   #img1에 넣기

            elif button == self.for_file_btn2:
                self.for_cvImage2 = cv2.imread(fileName)
                self.cvImage2 = cv2.resize(self.for_cvImage2, (600,400))
                height, width, byteValue = self.cvImage2.shape
                byteValue = byteValue * width
                cv2.cvtColor(self.cvImage2, cv2.COLOR_BGR2RGB, self.cvImage2)

                self.img2 = QImage(self.cvImage2, width, height, byteValue, QImage.Format_RGB888)


    def drawImages(self, painter):
        painter.drawImage(50, 50, self.img1)
        painter.drawImage(750, 50, self.img2)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.drawImages(painter)
        painter.end()