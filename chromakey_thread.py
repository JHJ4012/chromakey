from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class Thread(QThread):

    def get_info(self, fileName, side, QWidget):
        self.fileName = fileName
        self.edit = QWidget
        self.side = side
        self.while_control = True
        self.capture = cv2.VideoCapture(self.fileName)
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.delay = int(1000 / self.fps)
        self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.recoring = False
        if fileName != 0:
            self.edit.slider_video1.setMaximum(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.edit.start_video1.setEnabled(True)
            self.edit.stop_video1.setEnabled(True)
            self.edit.slider_video1.setEnabled(True)
        else:
            self.edit.slider_video1.setMaximum(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.edit.start_video1.setEnabled(False)
            self.edit.stop_video1.setEnabled(False)
            self.edit.slider_video1.setEnabled(False)

    def run(self):
        if self.capture:
            while self.while_control:
                if (self.capture.get(cv2.CAP_PROP_POS_FRAMES) == self.capture.get(cv2.CAP_PROP_FRAME_COUNT)):
                    break
                ret, self.frame = self.capture.read()
                video_capture = cv2.resize(self.frame, (600, 400))
                height, width, byteValue = video_capture.shape
                byteValue = byteValue * width
                cv2.cvtColor(video_capture, cv2.COLOR_BGR2RGB, video_capture)

                self.for_video_pixmap = QImage(video_capture, width, height, byteValue, QImage.Format_RGB888)
                pixmap_video = QPixmap.fromImage(self.for_video_pixmap)

                if self.fileName != 0:
                        self.edit.video1.setPixmap(pixmap_video)
                        self.edit.slider_video1.setValue(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
                else:
                    if self.side == "L":
                        self.edit.video1.setPixmap(pixmap_video)
                    elif self.side == "R":
                        self.edit.img2.setPixmap(pixmap_video)


                if self.recoring == True:
                    print('녹화중')
                    self.video.write(self.frame)

                cv2.waitKey(self.delay)

    def capture_camera(self, path):  # 사진 캡쳐
        self.path = path
        cv2.imwrite(self.path, self.frame)
        return self.path

    def record_camera(self, path):  # 녹화 시작
        self.path = path
        self.video = cv2.VideoWriter(self.path, self.fourcc, 20.0, (self.frame.shape[1], self.frame.shape[0]))
        self.recoring = True
        return self.path

    def stop_record(self):  # 녹화 중지
        self.recoring = False
        print("stop")
        self.video.release()
