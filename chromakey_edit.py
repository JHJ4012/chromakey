from PyQt5.QtGui import *
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

        self.start_video1 = QPushButton(self)       #비디오 컨트롤러
        self.start_video1.setGeometry(50,450,50,50)
        self.start_video1.clicked.connect(lambda state, button = self.start_video1 : self.startVideo(state,button))
        self.start_video1.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_video1.setIcon(QIcon('image/start.png'))
        self.start_video1.setIconSize(QSize(50,50))
        self.start_video1.setStyleSheet("border: 0px")

        self.stop_video1 = QPushButton(self)
        self.stop_video1.setGeometry(100,450,50,50)
        self.stop_video1.clicked.connect(lambda state, button = self.stop_video1 : self.stopVideo(state,button))
        self.stop_video1.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_video1.setIcon(QIcon('image/stop.png'))
        self.stop_video1.setIconSize(QSize(50,50))
        self.stop_video1.setStyleSheet("border: 0px")

        self.slider_video1 = QSlider(Qt.Horizontal, self)
        self.slider_video1.setGeometry(150,460,500,30)
        self.slider_video1.valueChanged.connect(lambda slider=self.slider_video1:self.changeValue(slider))
        self.slider_video1.sliderPressed.connect(lambda slider=self.slider_video1:self.pressSlider(slider))
        self.slider_video1.sliderReleased.connect(lambda slider=self.slider_video1:self.releaseSlider(slider))
        # self.slider_video1.sliderPressed.connect(lambda state, slider = self.slider_video1 : self.press_Slider(state, slider))
        # self.slider_video1.sliderReleased.connect(lambda state, slider = self.slider_video1 : self.release_Slider(state, slider))

        self.start_video1.hide()
        self.stop_video1.hide()
        self.slider_video1.hide()

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

        self.start_video2 = QPushButton(self)       #비디오 컨트롤러
        self.start_video2.setGeometry(750,450,50,50)
        self.start_video2.clicked.connect(lambda state, button=self.start_video2: self.startVideo(state, button))
        self.start_video2.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_video2.setIcon(QIcon('image/start.png'))
        self.start_video2.setIconSize(QSize(50,50))
        self.start_video2.setStyleSheet("border: 0px")

        self.stop_video2 = QPushButton(self)
        self.stop_video2.setGeometry(800,450,50,50)
        self.stop_video2.clicked.connect(lambda state, button=self.stop_video2: self.stopVideo(state, button))
        self.stop_video2.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_video2.setIcon(QIcon('image/stop.png'))
        self.stop_video2.setIconSize(QSize(50,50))
        self.stop_video2.setStyleSheet("border: 0px")

        self.slider_video2 = QSlider(Qt.Horizontal, self)
        self.slider_video2.setGeometry(850,460,500,30)
        self.slider_video2.valueChanged.connect(lambda slider = self.slider_video2 : self.changeValue(slider))
        self.slider_video2.sliderPressed.connect(lambda slider = self.slider_video2 : self.pressSlider(slider))
        self.slider_video2.sliderReleased.connect(lambda slider = self.slider_video2 : self.releaseSlider(slider))

        self.start_video2.hide()
        self.stop_video2.hide()
        self.slider_video2.hide()

        self.st_layout2.addWidget(self.img2)
        self.st_layout2.addWidget(self.video2)

        self.st_layout1.setCurrentIndex(0)  #최초에 창을 켰을 때는 둘 다 사진으로 시작
        self.st_layout2.setCurrentIndex(0)

        #기본 버튼 GUI
        self.for_file_btn1 = QPushButton('불러오기', self)
        self.for_file_btn1.setGeometry(550,510,100,50)
        self.for_file_btn1.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_file_btn1.clicked.connect(lambda state, button = self.for_file_btn1 : self.openFile(state, button))

        self.for_file_btn2 = QPushButton('불러오기', self)
        self.for_file_btn2.setGeometry(1250,510, 100,50)
        self.for_file_btn2.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_file_btn2.clicked.connect(lambda state, button = self.for_file_btn2 : self.openFile(state, button))

        self.for_webcam1 = QPushButton('촬영', self)
        self.for_webcam1.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_webcam1.setGeometry(440,510,100,50)

        self.for_webcam2 = QPushButton('촬영', self)
        self.for_webcam2.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_webcam2.setGeometry(1140,510,100,50)

        self.select_color_btn = QPushButton('색', self)
        self.select_color_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.select_color_btn.setGeometry(50, 510, 100, 50)

        self.test_label1 = QLabel(self)
        self.test_label1.setGeometry(50, 570, 600, 150)
        self.test_label1.setStyleSheet("background-color : red")

        self.test_label2 = QLabel(self)
        self.test_label2.setGeometry(750, 570, 600, 150)
        self.test_label2.setStyleSheet("background-color : red")

        self.back_first_window = QPushButton('처음으로', self)
        self.back_first_window.setGeometry(50, 730, 100, 50)
        self.back_first_window.setCursor(QCursor(Qt.PointingHandCursor))

        self.complete_btn = QPushButton('완료', self)
        self.complete_btn.setGeometry(1250,730,100,50)
        self.complete_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.th1 = Thread(self)
        self.th2 = Thread(self)

    def startVideo(self, state ,button):   #동영상 라디오 버튼 눌렀을 때 표시되고 동영상을 올리면 누르는거 가능하게.->누르기 전까지는 작동 안함.
                                            #start를 여기다가 함.
        if button == self.start_video1:
            self.th1.while_control = True
            if self.th1.capture.get(cv2.CAP_PROP_POS_FRAMES) == self.th1.capture.get(cv2.CAP_PROP_FRAME_COUNT):
                self.th1.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.th1.start()
        elif button == self.start_video2:
            self.th2.while_control = True
            if self.th2.capture.get(cv2.CAP_PROP_POS_FRAMES) == self.th2.capture.get(cv2.CAP_PROP_FRAME_COUNT):
                self.th2.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.th2.start()

    def stopVideo(self, state, button):
        if button == self.stop_video1:
            self.th1.while_control = False
        elif button == self.stop_video2:
            self.th2.while_control = False

    def changeValue(self, slider):
        if slider == self.slider_video1:
            print(self.slider_video1.value())
        elif slider == self.slider_video2:
            print(self.slider_video2.value())

    def pressSlider(self, slider):
        if slider == self.slider_video1:
            self.th1.while_control = False
        elif slider == self.slider_video2:
            self.th2.while_control = False

    def releaseSlider(self, slider):
        if slider == self.slider_video1:
            self.th1.capture.set(cv2.CAP_PROP_POS_FRAMES, self.slider_video1.value())
            self.th1.while_control = True
            self.th1.start()
        elif slider == self.slider_video2:
            self.th2.capture.set(cv2.CAP_PROP_POS_FRAMES, self.slider_video2.value())
            self.th2.while_control = True
            self.th2.start()

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

                self.th1.get_info(fileName, 0, self)
                self.th1.start()
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
                fileName, _ = QFileDialog.getOpenFileName(self, "불러올 동영상 ㄱㄱ", "", "Video Files (*.mp4 *.avi)")

                self.th2.get_info(fileName, 1, self)
                self.th2.start()

    #라디오 버튼에 연결되어 선택한 것 대로 위젯을 바꿔줌. 사진, 동영상에 맞게
    def change_mode(self, state, button):
        if button == self.radio1_photo:
            self.st_layout1.setCurrentIndex(0)
            self.start_video1.hide()
            self.stop_video1.hide()
            self.slider_video1.hide()
        elif button == self.radio1_video:
            self.st_layout1.setCurrentIndex(1)
            self.start_video1.show()
            self.stop_video1.show()
            self.slider_video1.show()
        elif button == self.radio2_photo:
            self.st_layout2.setCurrentIndex(0)
            self.start_video2.hide()
            self.stop_video2.hide()
            self.slider_video2.hide()
        elif button == self.radio2_video:
            self.st_layout2.setCurrentIndex(1)
            self.start_video2.show()
            self.stop_video2.show()
            self.slider_video2.show()

class Thread(QThread):

    def get_info(self, fileName, button, QWidget):
        self.fileName = fileName
        self.button = button
        self.edit = QWidget
        self.while_control = True
        if self.fileName:
            self.capture = cv2.VideoCapture(self.fileName)
            self.fps = self.capture.get(cv2.CAP_PROP_FPS)
            self.delay = int(1000 / self.fps)
            if self.button == 0:
                self.edit.slider_video1.setMaximum(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            elif self.button == 1:
                self.edit.slider_video2.setMaximum(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))

    def run(self):
        if self.capture:
            while self.while_control:
                if (self.capture.get(cv2.CAP_PROP_POS_FRAMES) == self.capture.get(cv2.CAP_PROP_FRAME_COUNT)):
                    break
                ret, frame = self.capture.read()
                video_capture = cv2.resize(frame, (600, 400))
                height, width, byteValue = video_capture.shape
                byteValue = byteValue * width
                cv2.cvtColor(video_capture, cv2.COLOR_BGR2RGB, video_capture)

                for_video_pixmap = QImage(video_capture, width, height, byteValue, QImage.Format_RGB888)
                pixmap_video = QPixmap.fromImage(for_video_pixmap)
                if self.button == 0:
                    self.edit.video1.setPixmap(pixmap_video)
                    self.edit.slider_video1.setValue(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
                elif self.button == 1:
                    self.edit.video2.setPixmap(pixmap_video)
                    self.edit.slider_video2.setValue(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
                cv2.waitKey(self.delay)
