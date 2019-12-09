from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import chromakey_thread, chromakey_first
import cv2, datetime, os

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

        self.box_layout1 = QHBoxLayout()

        self.group_box1.setLayout(self.box_layout1)

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


        self.st_layout1 = QStackedLayout()      #스택 레이아웃을 이용해 라디오 버튼이 사진일 때와 동영상일 때 바뀌도록.

        self.img1 = QLabel("이미지를 불러와주세요",self)               #pixmap 넣기 위한 label
        self.img1.setGeometry(50,50,600,400)
        self.img1.setAlignment(Qt.AlignCenter)
        self.img1.setStyleSheet("font-size : 20pt; font-family : '휴먼편지체'; border : 1px solid")
        self.img1.setCursor(QCursor(Qt.CrossCursor))

        self.video1 = QLabel("동영상을 불러와주세요",self)
        self.video1.setGeometry(50,50,600,400)
        self.video1.setAlignment(Qt.AlignCenter)
        self.video1.setStyleSheet("font-size : 20pt; font-family : '휴먼편지체'; border : 1px solid")
        self.video1.setCursor(QCursor(Qt.CrossCursor))

        self.start_video1 = QPushButton(self)       #비디오 컨트롤러
        self.start_video1.setGeometry(50,450,50,50)
        self.start_video1.clicked.connect(lambda state, button = self.start_video1 : self.startVideo(state,button))
        self.start_video1.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_video1.setIcon(QIcon('image/start.png'))
        self.start_video1.setIconSize(QSize(50,50))
        self.start_video1.setStyleSheet("border: 0px")
        self.start_video1.setDisabled(True)

        self.stop_video1 = QPushButton(self)
        self.stop_video1.setGeometry(100,450,50,50)
        self.stop_video1.clicked.connect(lambda state, button = self.stop_video1 : self.stopVideo(state,button))
        self.stop_video1.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_video1.setIcon(QIcon('image/stop.png'))
        self.stop_video1.setIconSize(QSize(50,50))
        self.stop_video1.setStyleSheet("border: 0px")
        self.stop_video1.setDisabled(True)

        self.slider_video1 = QSlider(Qt.Horizontal, self)
        self.slider_video1.setGeometry(150,460,500,30)
        self.slider_video1.valueChanged.connect(lambda slider=self.slider_video1:self.changeValue(slider))
        self.slider_video1.sliderPressed.connect(lambda slider=self.slider_video1:self.pressSlider(slider))
        self.slider_video1.sliderReleased.connect(lambda slider=self.slider_video1:self.releaseSlider(slider))
        self.slider_video1.setDisabled(True)
        self.slider_video1.setPageStep(0)

        self.start_video1.hide()
        self.stop_video1.hide()
        self.slider_video1.hide()

        self.st_layout1.addWidget(self.img1)
        self.st_layout1.addWidget(self.video1)

        self.img2 = QLabel("이미지를 불러와주세요",self)                #pixmap 넣기 위한 label
        self.img2.setGeometry(750,50,600,400)
        self.img2.setAlignment(Qt.AlignCenter)
        self.img2.setStyleSheet("font-size : 20pt; font-family : '휴먼편지체'; border : 1px solid")

        self.st_layout1.setCurrentIndex(0)  #최초에 창을 켰을 때는 사진으로 시작

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
        self.for_webcam1.clicked.connect(lambda state, button=self.for_webcam1: self.openWebcam(state, button))

        self.for_webcam2 = QPushButton('촬영', self)
        self.for_webcam2.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_webcam2.setGeometry(1140,510,100,50)
        self.for_webcam2.clicked.connect(lambda state, button=self.for_webcam2: self.openWebcam(state, button))

        self.for_color_label = QLabel('배경색 : ', self)
        self.for_color_label.setGeometry(50,510,100,50)
        self.for_color_label.setAlignment(Qt.AlignCenter)

        self.color_label = QLabel(self)
        self.color_label.setGeometry(150, 510, 50, 50)
        self.color_label.setStyleSheet("border : 1px solid")

        self.test_label1 = QLabel(self)
        self.test_label1.setGeometry(50, 570, 600, 150)
        self.test_label1.setStyleSheet("background-color : red")

        self.test_label2 = QLabel(self)
        self.test_label2.setGeometry(750, 570, 600, 150)
        self.test_label2.setStyleSheet("background-color : red")

        self.func1 = QPushButton('블러처리', self)
        self.func1.setCursor(QCursor(Qt.PointingHandCursor))
        self.func1.setGeometry(750, 510, 100, 50)
        self.func1.clicked.connect(lambda state, button=self.func1: self.effects(state, button))
        self.func1.setDisabled(True)  # 처음에 실행 했을 때 오른쪽 레이아웃에 사진이나 동영상이 없어서 비활성화

        self.return_img = QPushButton('되돌리기', self)
        self.return_img.setCursor(QCursor(Qt.PointingHandCursor))
        self.return_img.setGeometry(850, 510, 100, 50)
        self.return_img.clicked.connect(lambda state, button=self.return_img: self.effects(state, button))
        self.return_img.setDisabled(True)

        self.for_cap1 = QPushButton('사진 찍기', self)
        self.for_cap1.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_cap1.setGeometry(330, 730, 100, 50)
        self.for_cap1.clicked.connect(lambda state, button=self.for_cap1: self.capture(state, button))

        self.for_cap2 = QPushButton('사진 찍기', self)
        self.for_cap2.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_cap2.setGeometry(750, 730, 100, 50)
        self.for_cap2.clicked.connect(lambda state, button=self.for_cap2: self.capture(state, button))

        self.for_rec1 = QPushButton('녹화 시작', self)
        self.for_rec1.setCursor(QCursor(Qt.PointingHandCursor))
        self.for_rec1.setGeometry(440, 730, 100, 50)
        self.for_rec1.clicked.connect(lambda state, button=self.for_rec1: self.capture(state, button))

        self.rec_stop1 = QPushButton('녹화 종료', self)
        self.rec_stop1.setCursor(QCursor(Qt.PointingHandCursor))
        self.rec_stop1.setGeometry(550, 730, 100, 50)
        self.rec_stop1.clicked.connect(lambda state, button=self.rec_stop1: self.capture(state, button))

        self.back_first_window = QPushButton('처음으로', self)
        self.back_first_window.setGeometry(50, 730, 100, 50)
        self.back_first_window.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_first_window.clicked.connect(self.backToFirst)

        self.preview_btn = QPushButton('미리보기', self)
        self.preview_btn.setGeometry(1140,730,100,50)
        self.preview_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.preview_btn.clicked.connect(self.showPreview)

        self.complete_btn = QPushButton('저장', self)
        self.complete_btn.setGeometry(1250, 730, 100, 50)
        self.complete_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.error_label = QLabel('', self)
        self.error_label.setGeometry(860, 730, 270, 50)

        self.for_cap1.hide()
        self.for_cap2.hide()
        self.for_rec1.hide()
        self.rec_stop1.hide()

        self.th1 = chromakey_thread.Thread(self)  #왼쪽 스레드
        self.th2 = chromakey_thread.Thread(self)  #오른쪽 스레드

        self.color_photo = ''
        self.color_video = ''
    def mousePressEvent(self, event):
        if 50 <= event.pos().x() <= 650 and 50 <= event.pos().y() <= 450:
            if self.radio1_photo.isChecked():
                if self.img1.pixmap():
                    self.x = event.pos().x() - 50
                    self.y = event.pos().y() - 50
                    for_color = self.for_pixmap1.pixel(self.x,self.y)
                    self.color_photo = QColor(for_color).getHsv()[:-1]
                    self.color_label.setStyleSheet("border : 1px solid ; background: hsv" + str(self.color_photo) + ';')
                    print(self.color_photo)
            elif self.radio1_video.isChecked():
                if self.video1.pixmap():
                    self.x = event.pos().x() - 50
                    self.y = event.pos().y() - 50
                    for_color = self.th1.for_video_pixmap.pixel(self.x,self.y)
                    self.color_video = QColor(for_color).getHsv()[:-1]
                    self.color_label.setStyleSheet("border : 1px solid ; background: hsv" + str(self.color_video) + ';')


    def startVideo(self, state ,button):   #동영상 라디오 버튼 눌렀을 때 표시되고 동영상을 올리면 누르는거 가능하게.->누르기 전까지는 작동 안함.
                                            #start를 여기다가 함.
        if button == self.start_video1:
            self.th1.while_control = True
            if self.th1.capture.get(cv2.CAP_PROP_POS_FRAMES) == self.th1.capture.get(cv2.CAP_PROP_FRAME_COUNT):
                self.th1.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.th1.start()

    def stopVideo(self, state, button):
        self.th1.while_control = False

    def changeValue(self, slider):
        print(self.slider_video1.value())

    def pressSlider(self, slider):
        self.th1.while_control = False

    def releaseSlider(self, slider):
        self.th1.capture.set(cv2.CAP_PROP_POS_FRAMES, self.slider_video1.value())
        self.th1.while_control = True
        self.th1.start()

    #opencv를 이용해 화질을 더 좋게 변경
    def openFile(self, state, button):

        if button == self.for_file_btn1:
            if self.radio1_photo.isChecked():
                fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "Image Files (*.jpg *.png)")

                if fileName:
                    self.for_cvImage1 = cv2.imread(fileName)                    #opencv로 파일 불러옴
                    cvImage1 = cv2.resize(self.for_cvImage1, (600,400))    #불러온 파일 resize
                    height, width, byteValue = cvImage1.shape              #불러온 파일 정보 변수에 담기
                    byteValue = byteValue * width
                    cv2.cvtColor(cvImage1, cv2.COLOR_BGR2RGB, cvImage1)   #BGR을 RGB로 바꾸기

                    # dfdf = np.require(self.cvImage1, np.uint8, 'C')   #화질이 더 좋아진다는데 잘 모르겠음
                    self.for_pixmap1 = QImage(cvImage1, width, height, byteValue, QImage.Format_RGB888)   #img1에 넣기
                    pixmap_img1 = QPixmap.fromImage(self.for_pixmap1)
                    self.img1.setPixmap(pixmap_img1)
                    self.img1.setText('')

            elif self.radio1_video.isChecked():
                self.fileName1, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "Video Files (*.mp4 *.avi)")
                if self.fileName1:
                    self.th1.get_info(self.fileName1, "L",self)
                    self.th1.start()

        elif button == self.for_file_btn2:

            self.fileName, _ = QFileDialog.getOpenFileName(self, "불러올 이미지 ㄱㄱ", "", "Image Files (*.jpg *.png)")
            if self.fileName:
                self.for_cvImage2 = cv2.imread(self.fileName)
                cvImage2 = cv2.resize(self.for_cvImage2, (600,400))
                height, width, byteValue = cvImage2.shape
                byteValue = byteValue * width
                cv2.cvtColor(cvImage2, cv2.COLOR_BGR2RGB, cvImage2)

                for_pixmap2 = QImage(cvImage2, width, height, byteValue, QImage.Format_RGB888)
                pixmap_img2 = QPixmap.fromImage(for_pixmap2)
                self.img2.setPixmap(pixmap_img2)
                self.func1.setDisabled(False)

    def openWebcam(self, state, button):  # 카메라 켜기
        if button == self.for_webcam1:
            # self.radio1_camera.setChecked(True)
            # self.change_mode(True, self.radio1_camera)
            self.radio1_photo.setDisabled(True)
            self.radio1_video.setChecked(True)
            self.change_mode(True, self.radio1_video)

            self.for_cap1.show()
            self.for_rec1.show()
            self.rec_stop1.show()
            self.rec_stop1.setDisabled(True)
            self.for_file_btn1.setDisabled(True)

            self.th1.get_info(0, "L", self)
            self.th1.start()
        elif button == self.for_webcam2:
            self.for_cap2.show()
            self.for_file_btn2.setDisabled(True)

            self.th2.get_info(0, "R", self)
            self.th2.start()

    def capture(self, state, button):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        photo_path = os.path.join(str(now) + ".jpg")
        video_path = os.path.join(str(now) + ".mp4")

        # 왼쪽
        if button == self.for_cap1:  # 캡쳐
            cap = self.th1.capture_camera(photo_path)
            self.radio1_photo.setDisabled(False)
            self.radio1_photo.setChecked(True)
            self.change_mode(True, self.radio1_photo)
            self.th1.terminate()
            self.video1.setText("동영상을 불러와주세요")
            self.getPath(cap, "L")

        elif button == self.for_cap2:   #오른쪽 카메라 캡쳐
            cap = self.th2.capture_camera(photo_path)
            self.th2.terminate()
            self.getPath(cap, "R")

        elif button == self.for_rec1:  # 녹화 시작
            self.rec = self.th1.record_camera(video_path)
            self.rec_stop1.setDisabled(False)

        elif button == self.rec_stop1:  # 녹화 종료
            self.th1.stop_record()
            self.getPath(self.rec, "L")

    def getPath(self, path, side):  # webcam에서 저장한 파일 경로 받아서 화면에 적용

        control = path.split('.')[1]
        if control == 'jpg':
            self.fileName = path
        elif control == 'mp4':
            self.fileName1 = path

        if control == 'jpg':  # 사진 찍었을 때
            if side == "L":
                self.for_cvImage1 = cv2.imread(self.fileName)  # opencv로 파일 불러옴
                cvImage1 = cv2.resize(self.for_cvImage1, (600, 400))
                height, width, byteValue = cvImage1.shape  # 불러온 파일 정보 변수에 담기
                byteValue = byteValue * width
                cv2.cvtColor(cvImage1, cv2.COLOR_BGR2RGB, cvImage1)  # BGR을 RGB로 바꾸기

                self.for_pixmap1 = QImage(cvImage1, width, height, byteValue, QImage.Format_RGB888)  # img1에 넣기
                pixmap_img1 = QPixmap.fromImage(self.for_pixmap1)
                self.img1.setPixmap(pixmap_img1)
            elif side == "R":
                self.func1.setDisabled(False)
                self.return_img.setDisabled(False)
                self.for_cvImage2 = cv2.imread(self.fileName)  # opencv로 파일 불러옴
                cvImage2 = cv2.resize(self.for_cvImage2, (600, 400))
                height, width, byteValue = cvImage2.shape  # 불러온 파일 정보 변수에 담기
                byteValue = byteValue * width
                cv2.cvtColor(cvImage2, cv2.COLOR_BGR2RGB, cvImage2)  # BGR을 RGB로 바꾸기

                self.for_pixmap2 = QImage(cvImage2, width, height, byteValue, QImage.Format_RGB888)  # img1에 넣기
                pixmap_img2 = QPixmap.fromImage(self.for_pixmap2)
                self.img2.setPixmap(pixmap_img2)
                self.for_file_btn2.setDisabled(False)
                self.for_cap2.hide()

        elif control == 'mp4':  # 동영상 찍었을 때
            self.radio1_photo.setDisabled(False)
            self.radio1_video.setChecked(True)
            self.change_mode(True, self.radio1_video)
            self.th1.get_info(self.fileName1, "L", self)
            self.th1.start()

    def effects(self, state, button):
        for_cvImage1 = cv2.imread(self.fileName)
        cvImage1 = cv2.resize(for_cvImage1, (600, 400))
        height, width, byteValue = cvImage1.shape
        byteValue = byteValue * width
        cv2.cvtColor(cvImage1, cv2.COLOR_BGR2RGB, cvImage1)

        if button == self.func1:
            img_paint = cv2.blur(cvImage1, (10, 10))
            self.for_cvImage2 = cv2.cvtColor(img_paint, cv2.COLOR_RGB2BGR)

            self.for_pixmap2 = QImage(img_paint, width, height, byteValue, QImage.Format_RGB888)
            pixmap_img2 = QPixmap.fromImage(self.for_pixmap2)
            self.img2.setPixmap(pixmap_img2)
            self.return_img.setDisabled(False)
            self.func1.setDisabled(True)

        elif button == self.return_img:
            self.for_cvImage2 = cv2.cvtColor(cvImage1, cv2.COLOR_RGB2BGR)
            self.for_pixmap2 = QImage(cvImage1, width, height, byteValue, QImage.Format_RGB888)
            pixmap_img2 = QPixmap.fromImage(self.for_pixmap2)
            self.img2.setPixmap(pixmap_img2)
            self.return_img.setDisabled(True)
            self.func1.setDisabled(False)

#라디오 버튼에 연결되어 선택한 것 대로 위젯을 바꿔줌. 사진, 동영상에 맞게
    def change_mode(self, state, button):
        if button == self.radio1_photo:
            self.st_layout1.setCurrentIndex(0)
            self.start_video1.hide()
            self.stop_video1.hide()
            self.slider_video1.hide()
            self.for_cap1.hide()
            self.for_rec1.hide()
            self.rec_stop1.hide()
            self.for_file_btn1.setDisabled(False)
        elif button == self.radio1_video:
            self.st_layout1.setCurrentIndex(1)
            self.start_video1.show()
            self.stop_video1.show()
            self.slider_video1.show()
            self.for_cap1.hide()
            self.for_rec1.hide()
            self.rec_stop1.hide()
            self.for_file_btn1.setDisabled(False)

    def backToFirst(self):      #처음으로 돌아가면 작업 내용 초기화 해야되므로 self.close를 해줌. 나중에 진짜 나가시겠습니까? 라는 대화창 띄워주는 것 추가하기.
        reply = QMessageBox.question(self, 'Back to First', 'You really want to back to First Window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.first_window = chromakey_first.MainWindow()
            self.hide()
            self.first_window.show()        #back 했을 때에 no 누르면 first_window 뜸. 안 떠야됨

    def showPreview(self):              #preview로 갈 때 창이 꺼지지 않고 layout에서 widget이 바뀌는 형식으로 바꿈.
        # self.preview_window = chromakey_preview.PreviewWindow()
        # self.preview_window.show()
        self.make_Chromakey()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'You really want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def make_Chromakey(self):
        if self.radio1_photo.isChecked():

            if not self.img1.pixmap():                                      #예외처리 부분
                self.error_label.setText('왼쪽의 이미지를 불러와주세요')
                return
            elif not self.img2.pixmap():
                self.error_label.setText("오른쪽의 이미지를 불러와주세요")
                return
            elif self.color_photo == '':
                self.error_label.setText("색깔을 불러와주세요")
                return

            self.error_label.setText("")

            main_img = self.for_cvImage1
            background_img = self.for_cvImage2
            main_img = cv2.resize(main_img, (600, 400))
            background_img = cv2.resize(background_img, (600, 400))
            height1, width1 = main_img.shape[:2]
            height2, width2 = background_img.shape[:2]
            x = (width2 - width1) // 2
            y = height2 - height1
            w = x + width1
            h = y + height1
            # 뭔가 되긴 하는데 잘 안됨. 범위 이상한듯.
            # HSV로 바꾸니까 색깔이 반전되서 다른 색이 되버림. 그래서 안 되는거.
            # 배경색을 빨강, 초록, 파랑으로 제한시키는것은??
            offset = 20
            chromakey = main_img[self.y:self.y + 1, self.x:self.x + 1, :]

            hsv_chroma = cv2.cvtColor(chromakey, cv2.COLOR_BGR2HSV)
            hsv_img = cv2.cvtColor(main_img, cv2.COLOR_BGR2HSV)

            chroma_h = hsv_chroma[:, :, 0]
            lower = np.array([chroma_h.min() - offset, 40, 40])
            upper = np.array([chroma_h.max() + offset, 255, 255])
            mask = cv2.inRange(hsv_img, lower, upper)  # 대충 초록 파랑 빨강은 제대로 되는 것 같음.
            # mask = cv2.inRange(hsv_img, (0,0,0), (180,255,30)) #검은색
            # cv2.imshow('dffd', mask)
            mask_inv = cv2.bitwise_not(mask)
            roi = background_img[y:h, x:w]
            fg = cv2.bitwise_and(main_img, main_img, mask=mask_inv)
            bg = cv2.bitwise_and(roi, roi, mask=mask)
            background_img[y:h, x:w] = fg + bg
            cv2.imshow('dfdf', background_img)

        elif self.radio1_video.isChecked():
            
            if not self.video1.pixmap():                                #예외처리 부분
                self.error_label.setText('왼쪽의 영상을 불러와주세요')
                return
            elif not self.img2.pixmap():
                self.error_label.setText("오른쪽의 이미지를 불러와주세요")
                return
            elif self.color_video == '':
                self.error_label.setText("색깔을 불러와주세요")
                return
            self.error_label.setText("")

            background_img = self.for_cvImage2
            background_img = cv2.resize(background_img, (600, 400))
            cap = cv2.VideoCapture(self.fileName1)
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                delay = int(1000 / fps)

                while True:
                    if (cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT)):
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, img = cap.read()
                    if ret:
                        for_img = cv2.resize(img, (600, 400))
                        height1, width1 = for_img.shape[:2]
                        height2, width2 = background_img.shape[:2]
                        x = (width2 - width1) // 2
                        y = height2 - height1
                        w = x + width1
                        h = y + height1
                        # 뭔가 되긴 하는데 잘 안됨. 범위 이상한듯.
                        # HSV로 바꾸니까 색깔이 반전되서 다른 색이 되버림. 그래서 안 되는거.
                        # 배경색을 빨강, 초록, 파랑으로 제한시키는것은??
                        offset = 20
                        chromakey = for_img[self.y:self.y + 1, self.x:self.x + 1, :]
                        # chromakey = for_img[0:10, 0:10, :]

                        hsv_chroma = cv2.cvtColor(chromakey, cv2.COLOR_BGR2HSV)
                        hsv_img = cv2.cvtColor(for_img, cv2.COLOR_BGR2HSV)

                        chroma_h = hsv_chroma[:, :, 0]
                        lower = np.array([chroma_h.min() - offset, 40, 40])
                        upper = np.array([chroma_h.max() + offset, 255, 255])
                        mask = cv2.inRange(hsv_img, lower, upper)  # 대충 초록 파랑 빨강은 제대로 되는 것 같음.
                        # mask = cv2.inRange(hsv_img, (0,0,0), (180,255,30)) #검은색
                        mask_inv = cv2.bitwise_not(mask)
                        roi = background_img[y:h, x:w]
                        fg = cv2.bitwise_and(for_img, for_img, mask=mask_inv)
                        bg = cv2.bitwise_and(roi, roi, mask=mask)
                        for_img[y:h, x:w] = fg + bg
                        cv2.imshow('dfdf', for_img)
                        k = cv2.waitKey(delay) & 0xFF
                        if k == 27:
                            break
                    else:
                         break
            else:
                print("can't open video")
            cap.release()
            # cap.destroyAllWindows()