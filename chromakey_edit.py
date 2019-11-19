from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

class EditWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1400,800)

        #라디오 버튼 묶을 GroupBox
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

        #라디오 버튼 설정
        self.radio1_photo = QRadioButton("사진")
        self.radio1_video = QRadioButton("동영상")
        self.radio1_photo.setChecked(True)
        self.radio1_photo.clicked.connect(lambda state, button = self.radio1_photo : self.change_mode(state, button))
        self.radio1_video.clicked.connect(lambda state, button = self.radio1_video : self.change_mode(state, button))
        self.radio1_photo.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio1_video.setCursor(QCursor(Qt.PointingHandCursor))
        self.box_layout1.addWidget(self.radio1_photo)
        self.box_layout1.addWidget(self.radio1_video)

        self.radio2_photo = QRadioButton("사진")
        self.radio2_video = QRadioButton("동영상")
        self.radio2_photo.setChecked(True)
        self.radio2_photo.clicked.connect(lambda state, button = self.radio2_photo : self.change_mode(state, button))
        self.radio2_video.clicked.connect(lambda state, button = self.radio2_video : self.change_mode(state, button))
        self.radio2_photo.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio2_video.setCursor(QCursor(Qt.PointingHandCursor))
        self.box_layout2.addWidget(self.radio2_photo)
        self.box_layout2.addWidget(self.radio2_video)

        self.st_layout1 = QStackedLayout()      #스택 레이아웃을 이용해 라디오 버튼이 사진일 때와 동영상일 때 바뀌도록.

        self.img1 = QLabel("이미지를 불러와주세요",self)               #pixmap 넣기 위한 label
        self.img1.setGeometry(50,50,600,400)
        self.img1.setAlignment(Qt.AlignCenter)
        self.img1.setStyleSheet("font-size : 20pt; font-family : '휴먼편지체'; border : 1px solid")

        self.video1 = QLabel("동영상을 불러와주세요",self)
        self.video1.setGeometry(50,50,600,400)
        self.video1.setAlignment(Qt.AlignCenter)
        self.video1.setStyleSheet("font-size : 20pt; font-family : '휴먼편지체'; border : 1px solid")

        self.st_layout1.addWidget(self.img1)
        self.st_layout1.addWidget(self.video1)

        self.st_layout2 = QStackedLayout()      #스택 레이아웃을 이용해 라디오 버튼이 사진일 때와 동영상일 때 바뀌도록.

        self.img2 = QLabel("이미지를 불러와주세요",self)                #pixmap 넣기 위한 label
        self.img2.setGeometry(750,50,600,400)
        self.img2.setAlignment(Qt.AlignCenter)
        self.img2.setStyleSheet("font-size : 20pt; font-family : '휴먼편지체'; border : 1px solid")

        self.video2 = QLabel("동영상을 불러와주세요",self)
        self.video2.setGeometry(750,50,600,400)
        self.video2.setAlignment(Qt.AlignCenter)
        self.video2.setStyleSheet("font-size : 20pt; font-family : '휴먼편지체'; border : 1px solid")

        self.st_layout2.addWidget(self.img2)
        self.st_layout2.addWidget(self.video2)

        self.st_layout1.setCurrentIndex(0)  #최초에 창을 켰을 때는 둘 다 사진으로 시작
        self.st_layout2.setCurrentIndex(0)

        #기본 버튼 GUI
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

    #opencv를 이용해 화질을 더 좋게 변경
    def openFile(self, state, button):

        if button == self.for_file_btn1:
            if self.radio1_photo.isChecked():
                fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "Image Files (*.jpg *.png)")

                if fileName:
                    for_cvImage1 = cv2.imread(fileName)                    #opencv로 파일 불러옴
                    cvImage1 = cv2.resize(for_cvImage1, (600,400))    #불러온 파일 resize
                    height, width, byteValue = cvImage1.shape              #불러온 파일 정보 변수에 담기
                    byteValue = byteValue * width
                    cv2.cvtColor(cvImage1, cv2.COLOR_BGR2RGB, cvImage1)   #BGR을 RGB로 바꾸기

                    # dfdf = np.require(self.cvImage1, np.uint8, 'C')   #화질이 더 좋아진다는데 잘 모르겠음
                    for_pixmap1 = QImage(cvImage1, width, height, byteValue, QImage.Format_RGB888)   #img1에 넣기
                    pixmap_img1 = QPixmap.fromImage(for_pixmap1)
                    self.img1.setPixmap(pixmap_img1)

            elif self.radio1_video.isChecked():
                fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "Video Files (*.mp4 *.avi)")

                if fileName:
                    capture1 = cv2.VideoCapture(fileName)
                    fps = capture1.get(cv2.CAP_PROP_FPS)
                    delay = int(1000/fps)
                    while True:
                        if(capture1.get(cv2.CAP_PROP_POS_FRAMES) == capture1.get(cv2.CAP_PROP_FRAME_COUNT)):    #프레임이 다 돌아갔을 때 파일을 다시 열어 반복하게 해줌
                            capture1.open(fileName)
                        ret, frame = capture1.read()
                        video_capture1 = cv2.resize(frame, (600,400))
                        height, width, byteValue = video_capture1.shape
                        byteValue = byteValue * width
                        cv2.cvtColor(video_capture1, cv2.COLOR_BGR2RGB, video_capture1)

                        for_video_pixmap1 = QImage(video_capture1, width, height, byteValue, QImage.Format_RGB888)
                        pixmap_video1 = QPixmap.fromImage(for_video_pixmap1)
                        self.video1.setPixmap(pixmap_video1)

                        cv2.waitKey(delay)

        elif button == self.for_file_btn2:
            if self.radio2_photo.isChecked():
                fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "Image Files (*.jpg *.png)")
                if fileName:
                    for_cvImage2 = cv2.imread(fileName)
                    cvImage2 = cv2.resize(for_cvImage2, (600,400))
                    height, width, byteValue = cvImage2.shape
                    byteValue = byteValue * width
                    cv2.cvtColor(cvImage2, cv2.COLOR_BGR2RGB, cvImage2)

                    for_pixmap2 = QImage(cvImage2, width, height, byteValue, QImage.Format_RGB888)
                    pixmap_img2 = QPixmap.fromImage(for_pixmap2)
                    self.img2.setPixmap(pixmap_img2)

            elif self.radio2_video.isChecked():
                fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "Video Files (*.mp4 *.avi)")

                if fileName:
                    capture2 = cv2.VideoCapture(fileName)
                    fps = capture2.get(cv2.CAP_PROP_FPS)
                    delay = int(1000/fps)
                    while True:
                        if(capture2.get(cv2.CAP_PROP_POS_FRAMES) == capture2.get(cv2.CAP_PROP_FRAME_COUNT)):
                            capture2.open(fileName)
                        ret, frame = capture2.read()
                        video_capture2 = cv2.resize(frame, (600,400))
                        height, width, byteValue = video_capture2.shape
                        byteValue = byteValue * width
                        cv2.cvtColor(video_capture2, cv2.COLOR_BGR2RGB, video_capture2)

                        for_video_pixmap2 = QImage(video_capture2, width, height, byteValue, QImage.Format_RGB888)
                        pixmap_video2 = QPixmap.fromImage(for_video_pixmap2)
                        self.video2.setPixmap(pixmap_video2)

                        cv2.waitKey(delay)

    #라디오 버튼에 연결되어 선택한 것 대로 위젯을 바꿔줌. 사진, 동영상에 맞게
    def change_mode(self, state, button):
        if button == self.radio1_photo:
            self.st_layout1.setCurrentIndex(0)
        elif button == self.radio1_video:
            self.st_layout1.setCurrentIndex(1)
        elif button == self.radio2_photo:
            self.st_layout2.setCurrentIndex(0)
        elif button == self.radio2_video:
            self.st_layout2.setCurrentIndex(1)

