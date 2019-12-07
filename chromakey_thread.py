from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class Thread(QThread):

    def get_info(self, fileName, QWidget):
        self.fileName = fileName
        self.edit = QWidget
        self.while_control = True
        self.capture = cv2.VideoCapture(self.fileName)
        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.delay = int(1000 / self.fps)
        self.edit.slider_video1.setMaximum(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.edit.start_video1.setEnabled(True)
        self.edit.stop_video1.setEnabled(True)
        self.edit.slider_video1.setEnabled(True)

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

                self.for_video_pixmap = QImage(video_capture, width, height, byteValue, QImage.Format_RGB888)
                pixmap_video = QPixmap.fromImage(self.for_video_pixmap)
                self.edit.video1.setPixmap(pixmap_video)
                self.edit.slider_video1.setValue(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
